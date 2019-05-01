"""
-*- test-case-name: PyHouse.src.Modules.Housing.Entertainment.pandora.test.test_pandora -*-

@name: PyHouse/Project/src/Modules/Housing/Entertainment/pandora/pandora.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: (c)2014-2019 by D. Brian Kimmel
@note: Created on Feb 27, 2014
@license: MIT License
@summary: Controls pandora playback thru pianobar.

When PyHouse starts initially, Pandora is inactive.

When "pandora" button is pressed on a web page, pianobar is fired up as a process.

Further Mqtt messages control the pianobar process as needed, volume, next station etc.

When the stop button is pressed on a web page, pianobar is terminated and
this module goes back to its initial state ready for another session.

Now (2018) works with MQTT messages to control Pandora via PioanBar and PatioBar.
"""

__updated__ = '2019-04-20'
__version_info__ = (19, 4, 1)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
# import xml.etree.ElementTree as ET
from twisted.internet import protocol
from _datetime import datetime
from pathlib import Path

#  Import PyMh files and modules.
from Modules.Housing.Entertainment.pandora.pandora_xml import XML as pandoraXML
from Modules.Core.Utilities import extract_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Utilities.extract_tools import extract_quoted
# from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
from Modules.Housing.Entertainment.entertainment_data import \
        EntertainmentDeviceControl, \
        EntertainmentPluginData
# from Modules.Housing.Entertainment.entertainment_xml import XML as entertainmentXML

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Pandora        ')

PIANOBAR_LOCATION = '/usr/bin/pianobar'
SECTION = 'pandora'

#  (i) Control fifo at /home/briank/.config/pianobar/ctl opened


class PandoraStatusData():

    def __init__(self):
        self.Album = None
        self.Artist = None
        self.DateTimePlayed = None
        self.DateTimeStarted = None
        self.Error = None  # If some error occurred
        self.From = None  # This host id to identify where it came from
        self.inUseDevice = None
        self.Likability = None
        self.PlayingTime = None
        self.Song = None
        self.Station = None
        self.Status = 'Idle'  # Device if service is in use.


class PandoraControlData:
    """ Node-red interface allows some control of Pandora and hence the playback.
    This is it.
    """

    def __init__(self):
        self.Power = None
        self.Volume = None
        self.Like = None
        self.Dislike = None
        self.Skip = None


class MqttActions:
    """ Process messages to and from this module.
    Output Control messages use Mqtt to send messages to control the amplifier type device attached to the raspberry pi computer.
    Input Control messages come from a node red computer and are the listener (user) commands for their listening experience.
    """

    m_API = None
    m_transport = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _send_status(self, p_message):
            l_topic = 'entertainment/pandora/status'
            self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, p_message)

    def _send_control(self, p_device, p_message):
            l_topic = 'entertainment/{}/control'.format(p_device.ConnectionFamily)
            self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, p_message)

    def _decode_control(self, p_topic, p_message):
        """ Decode the message we just got.
         Someone (web page via node-red) wants to control pandora in some manner.

        ==> pyhouse/<house name>/entertainment/pandora/control/<do-this>
        <do-this> = On, Off, VolUp1, VolDown1, VolUp5, VolDown5, Like, Dislike

        We need to issue a message to control all connected devices.
        As a side effect, we need to control Pandora ( PianoBar ) via the control socket
        """
        l_logmsg = '\tPandora Control'
        # l_status = extract_tools.get_mqtt_field(p_message, 'Status')
        # l_sender = extract_tools.get_mqtt_field(p_message, 'Sender')
        l_power = extract_tools.get_mqtt_field(p_message, 'Power')
        l_volume = extract_tools.get_mqtt_field(p_message, 'Volume')
        # l_zone = extract_tools.get_mqtt_field(p_message, 'Zone')
        l_like = extract_tools.get_mqtt_field(p_message, 'Like')
        l_skip = extract_tools.get_mqtt_field(p_message, 'Skip')
        LOG.debug('{} {}'.format(p_topic, p_message))

        if l_power == 'On':
            l_logmsg += ' Turn On '
            l_power = 'On'
            l_input = extract_tools.get_mqtt_field(p_message, 'Input')
            self._play_pandora()
        elif l_power == 'PowerOff':
            l_logmsg += ' Turn Off '
            l_power = 'On'
            self._halt_pandora()

        elif l_volume == 'VolumeUp1':
            l_logmsg += ' Volume Up 1 '
            l_volume = 'VolumeUp1'
        elif l_volume == 'VolumeUp5':
            l_logmsg += ' Volume Up 5 '
            l_volume = 'VolumeUp5'
        elif l_volume == 'VolumeDown1':
            l_logmsg += ' Volume Down 1 '
            l_volume = 'VolumeDown1'
        elif l_volume == 'VolumeDown5':
            l_logmsg += ' Volume Down 5 '
            l_volume = 'VolumeDown5'

        elif l_like == 'LikeYes':
            l_logmsg += ' Like '
            l_like = 'Yes'
        elif l_like == 'LikeNo':
            l_logmsg += ' Dislike '
            l_like = 'No'

        elif l_skip == 'SkipYes':
            l_logmsg += ' Skip '
            l_skip = 'Yes'

        else:
            l_logmsg += ' Unknown Pandora Control Message {} {}'.format(p_topic, p_message)

        l_service = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        for l_device in l_service.Devices.values():
            l_obj = EntertainmentDeviceControl()
            l_obj.Device = l_device.ConnectionName
            l_obj.Family = l_device.ConnectionFamily
            l_obj.From = SECTION
            l_obj.InputName = l_input
            l_obj.Like = l_like
            l_obj.Power = l_power
            l_obj.Skip = l_skip
            l_obj.Volume = l_volume
            self._send_control(l_device, l_obj)
        return l_logmsg

    def decode(self, p_topic, p_message):
        """ Decode the Mqtt message
        We currently handle only control messages.
        We arenot interested in other peoples status.

        ==> pyhouse/<house name>/entertainment/pandora/<Action>/...
            where: <action> = control, status

        @param p_topic: is the topic after ',,,/pandora/'
        @return: the log message with information stuck in there.

        """
        l_logmsg = ' Pandora '
        if p_topic[0].lower() == 'control':
            l_logmsg += '\tPandora: {}\n'.format(self._decode_control(p_topic, p_message))
        elif p_topic[0].lower() == 'status':
            LOG.info('Status Msg: {} - {}'.format(p_topic, p_message))
        else:
            l_logmsg += '\tUnknown Pandora sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Entertainment msg', 160))
        return l_logmsg


class PianoBarProcessControl(protocol.ProcessProtocol):
    """ This handles the information coming back from pianobar concerning the playing song.
    """

    m_buffer = bytes()

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_buffer = bytes()

    def _extract_like(self, p_line):
        """ The like info comes back as a '<' in the now-playing info.
        """
        l_ix = p_line.find(b'<')
        if l_ix > 0:
            l_like = p_line[l_ix + 1:l_ix + 2].decode('utf-8')
            l_remain = p_line[:l_ix] + p_line[l_ix + 3:]
        else:
            l_like = ''
            l_remain = p_line
        return l_like, l_remain

    def _extract_station(self, p_line):
        """ Extract the station information from the now-playing message.
        """
        l_ix = p_line.find(b'@')
        l_sta = p_line[l_ix + 1:].decode('utf-8').strip()
        l_remain = p_line[:l_ix]
        return l_sta, l_remain

    def _extract_nowplaying(self, p_obj, p_playline):
        """
        """
        p_obj.From = self.m_pyhouse_obj.Computer.Name
        p_obj.DateTimePlayed = datetime.now()
        l_playline = p_playline
        p_obj.Song, l_playline = extract_quoted(l_playline, b'\"')
        p_obj.Artist, l_playline = extract_quoted(l_playline)
        p_obj.Album, l_playline = extract_quoted(l_playline)
        p_obj.Likability, l_playline = self._extract_like(l_playline)
        p_obj.Station, l_playline = self._extract_station(l_playline)
        p_obj.Status = 'Playing'
        return p_obj  # for debugging

    def _extract_playtime(self, p_obj, p_playline):
        """
        b'#   -03:00/03:00\r'
        """
        l_line = p_playline.strip()
        l_ix = l_line.find(b'/')
        p_obj.PlayingTime = l_line[l_ix + 1:].decode('utf-8')
        return p_obj

    def _extract_errors(self, p_playline):
        """
        """
        # l_title = extract_quoted(p_playline, b'\"')
        pass

    def _extract_line(self, p_line):
        """
        b'  "Carroll County Blues" by "Bryan Sutton" on "Not Too Far From The Tree" @ Bluegrass Radio'
        b'   "Love Is On The Way" by "Dave Koz" on "Greatest Hits" <3 @ Smooth Jazz Radio'
        b'\x1b[2K|>  "Mississippi Blues" by "Tim Sparks" on "Sidewalk Blues" <3 @ Acoustic Blues Radio\n'
        b'\x1b[2K#   -02:29/03:09\r'
        """
        # <ESC>[2K  Ansi esc sequence needs stripped off first.
        if p_line[0] == 0x1B:
            p_line = p_line[4:]
        if p_line[0] == b'q':
            LOG.info('Quitting Pandora')
            return
        if p_line.startswith(b'Welcome'):
            LOG.info(p_line)
            return
        if p_line.startswith(b'Press ? for'):
            return
        if p_line.startswith(b'Ok.'):
            return

        # Housekeeping messages Login, Rx Stations, Rx playlists, ...
        if p_line.startswith(b'(i)'):
            return

        # We gather the play data here but we do not send the message yet
        # We will wait for the first time to arrive.
        if p_line.startswith(b'|>'):  # This is
            self.m_time = None
            self.m_now_playing = PandoraStatusData()
            LOG.info("Playing: {}".format(p_line[2:]))
            self._extract_nowplaying(self.m_now_playing, p_line[2:])
            return
        # get the time and then send the message of now-playing
        if p_line.startswith(b'#'):
            if self.m_time == None:
                self.m_time = p_line[2:]
                self._extract_playtime(self.m_now_playing, p_line[2:])
                MqttActions(self.m_pyhouse_obj)._send_status(self.m_now_playing)
            return

        LOG.debug("Data = {}".format(p_line))
        pass

    def connectionMade(self):
        """Write to stdin.
        We do not have to do any initialization here.
        When we connect, the data flow from pianobar begins,
        """
        LOG.info("Connection to PianoBar Made.")

    def outReceived(self, p_data):
        """Data received from stdout.

        Note: Strings seem to begin with an ansi sequence  <esc>[xxx
        #        The line is a timestamp - every second
        (i)      This is an information message - Login, new playlist, etc.
        """
        self.m_buffer += p_data
        while self.m_buffer[0] == b'\n' or self.m_buffer[0] == b'\r':  # Strip off all leading newlines
            self.m_buffer = self.m_buffer[1:]
        while len(self.m_buffer) > 0:
            l_ix = self.m_buffer.find(b'\n')
            if l_ix > 0:
                l_line = self.m_buffer[:l_ix]
                self.m_buffer = self.m_buffer[l_ix + 1:]
                self._extract_line(l_line)
                continue
            else:
                l_line = self.m_buffer
                self._extract_line(l_line)
                self.m_buffer = bytes()

    def errReceived(self, p_data):
        """ Data received from StdErr.
        """
        LOG.warning("StdErr received - {}".format(p_data))


class PandoraControl:
    """
    """

    def _is_pianobar_installed(self):
        """
        """
        l_file = Path(PIANOBAR_LOCATION)
        if l_file.is_file():
            return True
        return False

    def _play_pandora(self):
        """ When we receive a proper Mqtt message to start (power on) the pandora player.
        We need to issue Mqtt messages to power on the sound system, set inputs, and a default volume.

        TO DO:
            Implement max play
        """
        l_service = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        LOG.debug('Play {}'.format(PrettyFormatAny.form(l_service, 'Pandora', 190)))
        if not self._is_pianobar_installed():
            self.m_started = False
            return
        if l_service._OpenSessions > 0:
            return
        l_service._OpenSessions += 1
        self.m_processProtocol = PianoBarProcessControl(self.m_pyhouse_obj)
        self.m_processProtocol.deferred = PianoBarProcessControl(self.m_pyhouse_obj)
        l_executable = PIANOBAR_LOCATION
        l_args = ('pianobar',)
        l_env = None  # this will pass <os.environ>
        self.m_transport = self.m_pyhouse_obj.Twisted.Reactor.spawnProcess(self.m_processProtocol, l_executable, l_args, l_env)
        self.m_started = True
        for l_device in l_service.Devices.values():
            l_obj = EntertainmentDeviceControl()
            l_name = l_device.ConnectionName
            l_family = l_device.ConnectionFamily
            l_topic = 'entertainment/{}/control'.format(l_family)
            l_obj.Family = l_family
            l_obj.Device = l_name
            l_obj.From = SECTION
            l_obj.Power = "On"
            l_obj.InputName = l_device.InputName
            l_obj.Volume = l_device.Volume
            LOG.info('Sending control-command to {}-{}'.format(l_family, l_name))
            self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_obj)

    def _halt_pandora(self):
        """ We have received a control message and therefore we stop the pandora player.
        This control message may come from a control screen or from a timer.
        """
        l_service = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        l_service._OpenSessions -= 1
        self.m_started = False
        self.m_transport.write(b'q')
        # self.m_transport.closeStdin()
        LOG.info('Service Stopped')
        for l_device in l_service.Devices.values():
            l_obj = EntertainmentDeviceControl()
            l_name = l_device.ConnectionName
            l_family = l_device.ConnectionFamily
            l_topic = 'entertainment/{}/control'.format(l_family)
            l_obj.Family = l_family
            l_obj.Device = l_name
            l_obj.From = SECTION
            l_obj.Power = "Off"
            l_obj.InputName = l_device.InputName
            l_obj.Volume = l_device.Volume
            LOG.info('Sending power off')
            self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_obj)
            LOG.info("Stopped Pandora.")

    def control_audio_device(self, p_audio_device, p_control):
        """
        """


class API(MqttActions, PandoraControl):

    m_started = False

    def __init__(self, p_pyhouse_obj):
        """ Do the housekeeping for the pandora plugin.
        """
        p_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        p_pyhouse_obj.House.Entertainment.Plugins[SECTION].Name = SECTION
        self.m_started = None
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_API = self
        LOG.info("API Initialized - Version:{}".format(__version__))

    def LoadXml(self, p_pyhouse_obj):
        """ Read the XML for pandora.
        """
        LOG.info("Loading XML - Version:{}".format(__version__))
        l_obj = pandoraXML().read_pandora_section_xml(p_pyhouse_obj)
        LOG.info("Loaded Pandora XML - Version:{}".format(__version__))
        if self._is_pianobar_installed():
            self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Active = False
            l_obj.Active = False
        return l_obj

    def Start(self):
        """ Start the Pandora plugin since we have it configured in the XML.
        This does not start playing pandora.  That takes a control message to play.
        """
        LOG.info("Started - Version:{}".format(__version__))
        l_pandora_obj = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        l_service = l_pandora_obj.Services[0]
        LOG.debug('{}'.format(PrettyFormatAny.form(l_service, 'Pandora', 190)))
        # l_device = l_service.ConnectionFamily.lower()
        # l_name = l_service.ConnectionName.lower()

    def SaveXml(self, _p_xml):
        """
        """
        l_xml = pandoraXML().write_pandora_section_xml(self.m_pyhouse_obj)
        LOG.info("Saved Pandora XML.")
        return l_xml

    def Stop(self):
        """Stop the Pandora player when we receive an IR signal to play some other thing.
        """
        self.m_started = False
        self.m_transport.write(b'q')
        self.m_transport.closeStdin()
        LOG.info("Stopped.")

# ## END DBK
