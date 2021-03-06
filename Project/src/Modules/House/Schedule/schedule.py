"""
@name:      Modules/House/Schedule/schedule.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Schedule events


Handle the home automation system schedule for a house.

The schedule is at the Core of PyHouse.
Lighting events, entertainment events, etc. for one house are triggered by the schedule and are run by twisted.

Read/reread the schedule file at:
    1. Start up
    2. Midnight
    3. After each set of scheduled events.


Controls:
    Communication
    Entertainment
    HVAC
    Irrigation
    Lighting
    Pool
    Security
    UPNP

Operation:

  Iterate thru the schedule tree and create a list of schedule events.
  Select the next event(s) from now, there may be more than one event scheduled for the same time.

  Create a twisted timer that goes off when the scheduled time arrives.
  We only create one timer (ATM) so that we do not have to cancel timers when the schedule is edited.
"""

__updated__ = '2020-02-17'
__version_info__ = (20, 1, 19)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import datetime
import aniso8601
# from typing import Optional

#  Import PyMh files
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.Utilities import convert, extract_tools
from Modules.House.Hvac.hvac_actions import Api as hvacActionsApi
from Modules.House.Irrigation.irrigation_action import Api as irrigationActionsApi
from Modules.House.Lighting.actions import Api as lightingActionsApi
from Modules.House.Lighting.utility import lightingUtility
from Modules.House.Schedule import ScheduleInformation
from Modules.House.Schedule.sunrisesunset import Api as sunriseApi

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Schedule       ')

SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = SECONDS_IN_MINUTE * 60  # 3600
SECONDS_IN_DAY = SECONDS_IN_HOUR * 24  # 86400
SECONDS_IN_WEEK = SECONDS_IN_DAY * 7  # 604800

INITIAL_DELAY = 5  # Must be from 5 to 30 seconds.
PAUSE_DELAY = 5
MINIMUM_TIME = 30  # We will not schedule items less than this number of seconds.  Avoid race conditions.
CONFIG_NAME = 'schedule'


class ScheduleEntertainmentInformation:
    """ This is the lighting specific part.
    """

    def __init__(self):
        self.Type = 'Lighting'
        self.Brightness = 0
        self.Name = None  # Light name
        self.Rate = 0
        self.Duration = None
        self.Room = None  # Room Name


class ScheduleLightingInformation:
    """ This is the lighting specific part.
    """

    def __init__(self):
        self.Type = 'Lighting'
        self.Brightness = 0
        self.Name = None  # Light name
        self.Rate = 0
        self.Duration = None
        self.Room = None  # Room Name


class ScheduleIrrigationInformation:
    """ This is the Irrigation specific part.
    """

    def __init__(self):
        self.Type = 'Irrigation'
        self.System = None
        self.Zone = None
        self.Duration = None


class ScheduleHvacInformation:
    """ This is the HVAC Thermostat specific part
    """

    def __init__(self):
        self.Type = 'Thermostat'


class RiseSet:

    def __init__(self):
        self.SunRise = None
        self.SunSet = None


class MqttActions:
    """ Schedule will react to some mqtt messages.
    Messages with the topic:
        ==> pyhouse/<housename>/house/schedule/<action>
    where <action> is:
        control:
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _add_schedule(self, p_message):
        """ A (remote) node has published a schedule - Add it to our schedules.
        """
        l_sender = extract_tools.get_mqtt_field(p_message, 'Sender')
        l_msg_obj = (p_message)
        # LOG.debug('Sched: {}\n{}'.format(p_message, PrettyFormatAny.form(l_msg_obj, 'Schedule', 190)))
        LOG.debug('Sched: {}\n{}'.format(p_message, l_msg_obj))
        if l_sender == self.m_pyhouse_obj.Computer.Name:
            return
        l_name = extract_tools.get_mqtt_field(p_message, 'LightName')
        l_light_obj = lightingUtility().get_object_type_by_id(self.m_pyhouse_obj.House.Lighting.Lights, name=l_name)
        if l_light_obj == None:
            return
        l_key = len(self.m_pyhouse_obj.House.Schedules)
        l_sched = ScheduleInformation()
        l_sched.Name = l_name
        l_sched.Key = l_key
        # l_sched.Active = True
        l_sched.Comment = extract_tools.get_mqtt_field(p_message, 'Comment')
        l_sched.LastUpdate = datetime.datetime.now()
        l_sched.UUID = extract_tools.get_mqtt_field(p_message, 'UUID')
        l_sched.DayOfWeek = extract_tools.get_mqtt_field(p_message, 'DayOfWeek')
        l_sched.ScheduleMode = extract_tools.get_mqtt_field(p_message, 'ScheduleMode')
        l_sched.Sched.Type = extract_tools.get_mqtt_field(p_message, 'Sched.Type')
        l_sched.Time = extract_tools.get_mqtt_field(p_message, 'Time')
        l_sched.Level = extract_tools.get_mqtt_field(p_message, 'Level')
        l_sched.LightName = extract_tools.get_mqtt_field(p_message, 'LightName')
        l_sched.LightUUID = extract_tools.get_mqtt_field(p_message, 'LightUUID')
        l_sched.Rate = extract_tools.get_mqtt_field(p_message, 'Rate')
        l_sched.RoomName = extract_tools.get_mqtt_field(p_message, 'RoomName')
        l_sched.RoomUUID = extract_tools.get_mqtt_field(p_message, 'RoomUUID')
        LOG.debug('Schedule added locally: {}'.format(PrettyFormatAny.form(l_sched, 'Schedule', 190)))

    def decode(self, p_msg):
        """
        --> pyhouse/<housename>/house/schedule/...
        """
        l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        l_schedule_type = extract_tools.get_mqtt_field(p_msg.Payload, 'Sched.Type')
        l_light_name = extract_tools.get_mqtt_field(p_msg.Payload, 'LightName')
        l_light_level = extract_tools.get_mqtt_field(p_msg.Payload, 'Level')
        if len(p_msg.Topic) > 0:
            if l_topic[0] == 'control':
                p_msg.LogMessage += '\tExecute:\n'
                p_msg.LogMessage += '\tType: {}\n'.format(l_schedule_type)
                p_msg.LogMessage += '\tLight: {}\n'.format(l_light_name)
                p_msg.LogMessage += '\tLevel: {}'.format(l_light_level)
                self._add_schedule(p_msg.Payload)
            elif l_topic[0] == 'status':
                p_msg.LogMessage += '\tStatus:\n'
                p_msg.LogMessage += '\tType: {}\n'.format(l_schedule_type)
                p_msg.LogMessage += '\tLight: {}\n'.format(l_light_name)
                p_msg.LogMessage += '\tLevel: {}'.format(l_light_level)
            elif l_topic[0] == 'control':
                p_msg.LogMessage += '\tControl:\n'
            elif l_topic[0] == 'delete':
                pass
            elif l_topic[0] == 'update':
                pass
            else:
                p_msg.LogMessage += '\tUnknown sub-topic: {}; - {}'.format(p_msg.Topic, p_msg.Payload)
                LOG.warning('Unknown Schedule Topic: {}'.format(p_msg.Topic[0]))


class DOW:
    """ Day of week.
    """


class TimeField:
    """ This class deals with the Time Field parsing.

        Possible valid formats are:
        hh
        hh:mm
        hh:mm:ss
        sunrise
        sunrise + hh
        sunrise + hh:mm
        sunrise + hh:mm:ss
        sunrise - hh
        sunrise - hh:mm
        sunrise - hh:mm:ss
    """

    m_seconds = 0

    def _rise_set(self, p_timefield, p_rise_set):
        """
        """
        l_seconds = 0
        l_timefield = p_timefield.lower().strip()
        if 'dawn' in l_timefield:
            l_seconds = convert.datetime_to_seconds(p_rise_set.Dawn)
            l_timefield = l_timefield[4:].strip()
        elif 'sunrise' in l_timefield:
            l_seconds = convert.datetime_to_seconds(p_rise_set.SunRise)
            l_timefield = l_timefield[7:].strip()
        elif 'noon' in l_timefield:
            # print('Noon - {}'.format(l_timefield))
            l_seconds = convert.datetime_to_seconds(p_rise_set.Noon)
            l_timefield = l_timefield[4:].strip()
        elif 'sunset' in l_timefield:
            # print('SunSet - {}'.format(l_timefield))
            l_seconds = convert.datetime_to_seconds(p_rise_set.SunSet)
            l_timefield = l_timefield[6:].strip()
        elif 'dusk' in l_timefield:
            # print('Dusk - {}'.format(l_timefield))
            l_seconds = convert.datetime_to_seconds(p_rise_set.Dusk)
            l_timefield = l_timefield[4:].strip()
        else:
            l_seconds = 0
        self.m_seconds = l_seconds
        return l_timefield, l_seconds

    def _extract_sign(self, p_timefield):
        """
        """
        l_timefield = p_timefield.strip()
        l_subflag = False
        if '-' in l_timefield:
            l_subflag = True
            l_timefield = l_timefield[1:]
        elif '+' in l_timefield:
            l_subflag = False
            l_timefield = l_timefield[1:]
        l_timefield = l_timefield.strip()
        return l_timefield, l_subflag

    def _extract_time_part(self, p_timefield):
        """
        """
        try:
            l_time = aniso8601.parse_time(p_timefield)
        except Exception:
            l_time = datetime.time(0)
        return convert.datetime_to_seconds(l_time)

    def parse_timefield(self, p_timefield, p_rise_set):
        """
        """
        l_timefield, l_seconds = self._rise_set(p_timefield, p_rise_set)
        l_timefield, l_subflag = self._extract_sign(l_timefield)
        l_offset = self._extract_time_part(l_timefield)
        if l_subflag:
            l_seconds -= l_offset
        else:
            l_seconds += l_offset
        return l_seconds

    def get_timefield_seconds(self):
        return self.m_seconds


class TimeCalcs:
    """
    Get the when scheduled time.
    It may be from about a minute to about 1 week.
    If the schedule is not active return a None.

    The config file caries DOW as a seven charicter string 'SMTWTFS' where the DOW letter is replaced by a dash '-' if inactive.
    Therefore wednesday only will be represented by '---W---'
    This class deals with extracting information from the time and DayOfWeek fields of a schedule.

    DayOfWeek        mon=1, tue=2, wed=4, thu=8, fri=16, sat=32, sun=64
    weekday          mon=0, tue=1, wed=2, thu=3, fri=4,  sat=5,  sun=6

    The time field may be:
        HH:MM or HH:MM:SS
        sunrise/sunset/dawn/dusk  +/-  offset HH:MM:SS or HH:MM
    """

    def _extract_days(self, p_schedule_obj, p_now):
        """ Get the number of days until the next DayOfWeek in the schedule.

        DayOfWeek        mon=1, tue=2, wed=4, thu=8, fri=16, sat=32, sun=64
        weekday()        mon=0, tue=1, wed=2, thu=3, fri=4,  sat=5,  sun=6

        @param p_schedule_obj: is the schedule object we are working on
        @param p_now: is a datetime.datetime.now()
        @return: the number of days till the next DayOfWeek - 0..6, 10 if never
        """
        l_dow = p_schedule_obj.DOW

        return 0

        l_now_day = p_now.weekday()
        l_day = 2 ** l_now_day
        l_is_in_dow = (l_dow & l_day) != 0
        if l_is_in_dow:
            return 0
        l_days = 1
        for _l_ix in range(0, 7):
            l_now_day = (l_now_day + 1) % 7
            l_day = 2 ** l_now_day
            l_is_in_dow = (l_dow & l_day) != 0
            if l_is_in_dow:
                return l_days
            l_days += 1
        return 10

    def extract_time_to_go(self, p_schedule_obj, p_now, p_rise_set):
        """ Compute the seconds to go from now to the next scheduled time.
        May be from 30 seconds to a full week.

        @param p_schedule_obj: is the schedule object we are working on.
        @param p_now: is the datetime for now.
        @param p_rise_set: is the sunrise/sunset structure.
        @return: The number of seconds from now to the scheduled time.
        """
        l_dow_seconds = TimeCalcs()._extract_days(p_schedule_obj, p_now) * 24 * 60 * 60
        l_sched_seconds = TimeField().parse_timefield(p_schedule_obj.Time, p_rise_set)
        l_sched_secs = l_dow_seconds + l_sched_seconds
        l_now_seconds = convert.datetime_to_seconds(p_now)
        l_seconds = l_sched_secs - l_now_seconds
        if l_seconds < 0:
            l_seconds += SECONDS_IN_DAY
        return l_seconds


class ScheduleExecution:

    def dispatch_one_schedule(self, p_pyhouse_obj, p_schedule_obj):
        """
        Send information to one device to execute a schedule.
        @param p_schedule_obj: ==> ScheduleInformation()
        """
        l_topic = 'house/schedule/control'
        l_obj = p_schedule_obj
        p_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, l_obj)
        #
        if p_schedule_obj.Sched.Type in ['Lighting', 'Light', 'Outlet']:
            LOG.info('Execute_one_schedule type = Lighting - "{}"'.format(p_schedule_obj.Sched.Name))
            lightingActionsApi().DoSchedule(p_pyhouse_obj, p_schedule_obj)
        #
        elif p_schedule_obj.Sched.Type == 'Hvac':
            LOG.info('Execute_one_schedule type = Hvac')
            hvacActionsApi().DoSchedule(p_pyhouse_obj, p_schedule_obj)
        #
        elif p_schedule_obj.Sched.Type == 'Irrigation':
            LOG.info('Execute_one_schedule type = Irrigation')
            irrigationActionsApi().DoSchedule(p_pyhouse_obj, p_schedule_obj)
        #
        elif p_schedule_obj.Sched.Type == 'TeStInG14159':  # To allow a path for unit tests
            LOG.info('Execute_one_schedule type = Testing')
            #  scheduleActionsApi().DoSchedule(p_pyhouse_obj, p_schedule_obj)
        #
        else:
            LOG.error('Unknown schedule type: {}'.format(p_schedule_obj.Sched.Type))
            irrigationActionsApi().DoSchedule(p_pyhouse_obj, p_schedule_obj)

    @staticmethod
    def execute_schedules_list(p_pyhouse_obj, p_key_list=[]):
        """ The timer calls this with a list of schedules to be executed.

        For each Schedule in the list, call the dispatcher for that type of schedule.

        Delay before generating the next schedule to avoid a race condition
         that duplicates an event if it completes before the clock goes to the next second.

        @param p_key_list: a list of schedule keys in the next time schedule to be executed.
        """
        LOG.info("About to execute - Schedule Items:{}".format(p_key_list))
        for l_slot in p_key_list:
            l_schedule_obj = p_pyhouse_obj.House.Schedules[l_slot]
            ScheduleExecution().dispatch_one_schedule(p_pyhouse_obj, l_schedule_obj)
        lightingUtilitySch(p_pyhouse_obj).schedule_next_event()


class lightingUtilitySch:
    """
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _fetch_sunrise_set(self):
        _l_topic = 'house/schedule/sunrise_set'
        l_riseset = self.m_pyhouse_obj.House.Location._RiseSet
        LOG.info('Got Sunrise: {};   Sunset: {}'.format(l_riseset.SunRise, l_riseset.SunSet))
        return l_riseset

    def _find_next_scheduled_events(self):
        """ Go thru all the schedules and find the next schedule list to run.
        Note that there may be several scheduled events for that time

        @return: a delay time to the next event chain, and a list of events in the chain.
        """
        self.m_pyhouse_obj = self.m_pyhouse_obj
        l_now = datetime.datetime.now()  # Freeze the current time so it is the same for every event in the list.
        l_schedule_key_list = []
        l_current_delay = SECONDS_IN_WEEK  # Start the search with a very long time to go
        l_riseset = self._fetch_sunrise_set()
        # Loop through the possible scheduled events.
        for l_key, l_schedule_obj in self.m_pyhouse_obj.House.Schedules.items():
            l_seconds = TimeCalcs().extract_time_to_go(l_schedule_obj, l_now, l_riseset)
            # Avoid race donditions by having a minimum time.
            if l_seconds < MINIMUM_TIME:
                continue
            # If the time is the same as the current list of collected times, add this entry to the list.
            if l_current_delay == l_seconds:  # Add to lists for the given time.
                l_schedule_key_list.append(l_key)
            # If we found an earlier time, abandon the old list and start a new list with this time.
            elif l_seconds < l_current_delay:  # earlier schedule - start new list
                l_current_delay = l_seconds
                l_schedule_key_list = []
                l_schedule_key_list.append(l_key)
        l_debug_msg = "Delaying {} for list {}".format(l_current_delay, l_schedule_key_list)
        LOG.info("find next scheduled events complete. {}".format(l_debug_msg))
        return l_current_delay, l_schedule_key_list

    def run_after_delay(self, p_delay, p_list):
        """
        """
        l_runID = self.m_pyhouse_obj._Twisted.Reactor.callLater(p_delay, ScheduleExecution.execute_schedules_list, self.m_pyhouse_obj, p_list)
        l_datetime = datetime.datetime.fromtimestamp(l_runID.getTime())
        LOG.info('Scheduled {} after delay of {} - Time: {}'.format(p_list, p_delay, l_datetime))
        return l_runID

    def schedule_next_event(self, p_delay=0):
        """ Find the list of schedules to run, call the timer to run at the time in the schedules.

        This is the main schedule loop.
        It may be restarted if the schedules change.

        Scans through the list of scheduled events.
        Picks out all the events next to perform (there may be several).
        Puts all the events in a list.
        Schedules an execution event on the list of scheduled events.

        @param p_delay: is the (forced) delay time for the timer.
        """
        l_delay, l_list = self._find_next_scheduled_events()
        if p_delay != 0:
            l_delay = p_delay
        lightingUtilitySch(self.m_pyhouse_obj).run_after_delay(l_delay, l_list)

    def XXXfind_all_schedule_entries(self, p_pyhouse_obj, p_type=None):
        """ Find all the schedule entry using any of several criteria.
        Type (required)
        Mode (required)

        @return: a list schedule objects, None if error or no matches.
        """
        l_sched_list = []
        l_scheds = p_pyhouse_obj.House.Schedules
        for l_sched in  l_scheds.values():
            # print('sched', l_sched.Name)
            if l_sched.Sched.Type == p_type:
                # print('sched', l_sched.Name)
                l_sched_list.append(l_sched)
        if len(l_sched_list) == 0:
            return None
        return l_sched_list


class Timers:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_timers = {}
        self.m_count = 0

    def set_one(self, p_pyhouse_obj, p_delay, p_list):
        l_callback = ScheduleExecution.execute_schedules_list
        l_runID = p_pyhouse_obj._Twisted.Reactor.callLater(p_delay, l_callback, p_pyhouse_obj, p_list)
        l_datetime = datetime.datetime.fromtimestamp(l_runID.getTime())
        LOG.info('Scheduled {} after delay of {} - Time: {}'.format(p_list, p_delay, l_datetime))
        return l_runID


class LocalConfig:
    """ This will handle reading and writing of the schedule.yaml config file.
    """

    m_config = None
    m_pyhouse_obj = None
    m_schedule_altered = False

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)
        self.m_schedule_altered = False

    def _extract_entertainment_schedule(self, p_config):
        """
        """
        l_obj = ScheduleEntertainmentInformation()
        for l_key, l_value in p_config.items():
            setattr(l_obj, l_key, l_value)
        return l_obj

    def _extract_irrigation_schedule(self, p_config):
        """
        """
        l_obj = ScheduleIrrigationInformation()
        for l_key, l_value in p_config.items():
            setattr(l_obj, l_key, l_value)
        return l_obj

    def _extract_lighting_schedule(self, p_config, p_key):
        """
        """
        l_obj = ScheduleLightingInformation()
        l_obj.Type = p_key
        for l_key, l_value in p_config.items():
            # LOG.debug('Lighting Key:{}; Value:{}'.format(l_key, l_value))
            setattr(l_obj, l_key, l_value)
        return l_obj

    def _extract_outlet_schedule(self, p_config):
        """
        """
        l_obj = ScheduleLightingInformation()
        l_obj.Type = 'Outlet'
        for l_key, l_value in p_config.items():
            setattr(l_obj, l_key, l_value)
        return l_obj

    def _extract_hvac_schedule(self, p_config):
        """
        """
        l_obj = ScheduleHvacInformation()
        for l_key, l_value in p_config.items():
            setattr(l_obj, l_key, l_value)
        return l_obj

    def _extract_DOW_field(self, p_config):
        """
        """
        l_dow = p_config.upper()
        _l_ret = 0
        if len(l_dow) != 7:
            LOG.error('Day of week must be 7 chars long "--TWT--" was "{}"'.format(l_dow))
            return 127
        return l_dow

    def _extract_one_schedule(self, p_config):
        """ Extract a complete schedule configuration entry.
        """
        l_required = ['Name', 'Occupancy', 'DOW', 'Time', 'Sched']
        l_obj = ScheduleInformation()
        for l_key, l_value in p_config.items():
            if l_key == 'Entertainment':
                pass
            elif l_key == 'Irrigation':
                l_obj.Sched = self._extract_irrigation_schedule(l_value)
            elif l_key in ['Lighting', 'Light', 'Outlet']:
                l_obj.Sched = self._extract_lighting_schedule(l_value, l_key)
            elif l_key in ['Hvac', 'Thermostat']:
                l_obj.Sched = self._extract_hvac_schedule(l_value)
            elif l_key == 'DOW':
                l_obj.DOW = self._extract_DOW_field(l_value)
            elif l_key == 'Occupancy':
                pass
            elif l_key == 'Room':
                l_obj.Room = self.m_config.extract_room_group(l_value)
            else:
                setattr(l_obj, l_key, l_value)
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('Schedule config file is missing an entry for "{}"'.format(l_key))
        LOG.info('Extracted Schedule "{}"'.format(l_obj.Name))
        return l_obj

    def _extract_all_schedules(self, p_config):
        """
        """
        l_scheds = {}
        for l_ix, l_value in enumerate(p_config):
            l_obj = self._extract_one_schedule(l_value)
            l_scheds[l_ix] = l_obj
        LOG.info('Extracted {} Schedules'.format(len(l_scheds)))
        return l_scheds

    def load_yaml_config(self):
        """
        """
        # LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj.House.Schedules = None
        l_yaml = self.m_config.read_config_file(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Schedules']
        except:
            LOG.warning('The config file does not start with "Schedules:"')
            return None
        l_scheds = self._extract_all_schedules(l_yaml)
        self.m_pyhouse_obj.House.Schedules = l_scheds
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Schedules[0], 'Schedule[0]'))
        return l_scheds  # for testing purposes

# ----------

    def save_yaml_config(self):
        """
        """


class Api:

    m_pyhouse_obj = None
    m_local_config = None

    def __init__(self, p_pyhouse_obj):
        LOG.info("Initializing - Version:{}".format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        self.m_sunrise_api = sunriseApi(p_pyhouse_obj)

    def _add_storage(self):
        """
        """
        self.m_pyhouse_obj.House.Schedules = {}

    def LoadConfig(self):
        """ Load the Schedule from the Config info.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj.House.Schedules = {}
        l_schedules = self.m_local_config.load_yaml_config()
        # LOG.info('Loaded {} Schedules.'.format(len(self.m_pyhouse_obj.House.Schedules)))
        return l_schedules  # for testing

    def Start(self):
        """
        Extracts all from XML so an update will write correct info back out to the XML file.
        """
        LOG.info("Starting.")
        self.m_sunrise_api.Start()
        self.m_pyhouse_obj._Twisted.Reactor.callLater(INITIAL_DELAY, lightingUtilitySch(self.m_pyhouse_obj).schedule_next_event)
        LOG.info("Started.")

    def Stop(self):
        """Stop everything.
        """
        LOG.info("Stopped.")

    def SaveConfig(self):
        """
        """
        self.m_local_config.save_yaml_config()
        LOG.info('Saved Schedules Config.')

# ## END DBK
