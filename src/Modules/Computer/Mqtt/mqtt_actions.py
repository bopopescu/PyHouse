"""
@name:      PyHouse/src/Modules/Computer/Mqtt/mqtt_actions.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created Feb 20, 2016
@Summary:

"""

__updated__ = '2017-03-11'

from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.data_objects import NodeData
from Modules.Housing.Entertainment.entertainment import MqttActions as entertainmentMqtt
from Modules.Housing.Security.security import MqttActions as securityMqtt


class Actions(object):
    """
    """
    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_myname = p_pyhouse_obj.Computer.Name

    def _get_field(self, p_message, p_field):
        try:
            l_ret = p_message[p_field]
        except (KeyError, TypeError):
            l_ret = 'The "{}" field was missing in the MQTT Message.'.format(p_field)
        return l_ret

    def _extract_node(self, p_message):
        l_node = NodeData()
        l_node.Name = self._get_field(p_message, 'Name')
        l_node.Key = l_node.Name
        l_node.Active = True
        l_node.Comment = ''
        l_node.ConnectionAddr_IPv4 = self._get_field(p_message, 'ConnectionAddr_IPv4')
        l_node.ConnectionAddr_IPv6 = self._get_field(p_message, 'ConnectionAddr_IPv6')
        l_node.ControllerCount = self._get_field(p_message, 'ControllerCount')
        l_node.ControllerTypes = self._get_field(p_message, 'ControllerTypes')
        l_node.NodeId = self._get_field(p_message, 'NodeId')
        l_node.NodeRole = self._get_field(p_message, 'NodeRole')

    def _decode_hvac(self, p_logmsg, _p_topic, p_message):
        p_logmsg += '\tThermostat:\n'
        p_logmsg += '\tName: {}'.format(self.m_name)
        p_logmsg += '\tRoom: {}\n'.format(self.m_room_name)
        p_logmsg += '\tTemp: {}'.format(self._get_field(p_message, 'CurrentTemperature'))
        return p_logmsg

    def _decode_lighting(self, p_logmsg, _p_topic, p_message):
        p_logmsg += '\tLighting:\n'
        p_logmsg += '\tName: {}\n'.format(self.m_name)
        p_logmsg += '\tRoom: {}\n'.format(self.m_room_name)
        p_logmsg += '\n\tLevel: {}'.format(self._get_field(p_message, 'CurLevel'))
        return p_logmsg

    def _decode_room(self, p_logmsg, p_topic, p_message):
        p_logmsg += '\tRooms:\n'
        if p_topic[1] == 'add':
            p_logmsg += '\tName: {}\n'.format(self._get_field(p_message, 'Name'))
        elif p_topic[1] == 'delete':
            p_logmsg += '\tName: {}\n'.format(self._get_field(p_message, 'Name'))
        else:
            p_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Rooms msg', 160))
        return p_logmsg

    def _decode_schedule(self, p_logmsg, p_topic, p_message):
        p_logmsg += '\tSchedule:\n'
        if p_topic[1] == 'execute':
            p_logmsg += '\tType: {}\n'.format(self._get_field(p_message, 'ScheduleType'))
            p_logmsg += '\tRoom: {}\n'.format(self.m_room_name)
            p_logmsg += '\tLight: {}\n'.format(self._get_field(p_message, 'LightName'))
            p_logmsg += '\tLevel: {}'.format(self._get_field(p_message, 'Level'))
        else:
            p_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Schedule msg', 160))
        return p_logmsg

    def _decode_weather(self, p_logmsg, _p_topic, p_message):
        p_logmsg += '\tWeather:\n'
        l_temp = float(self._get_field(p_message, 'Temperature'))
        p_logmsg += '\tName: {}\n'.format(self._get_field(p_message, 'Location'))
        p_logmsg += '\tTemp: {} ({})'.format(l_temp, ((l_temp / 5.0) * 9.0) + 32.0)
        p_logmsg += '\tWeather info {}'.format(PrettyFormatAny.form(p_message, 'Weather msg', 160))
        return p_logmsg

    def _decodeLWT(self, p_logmsg, p_topic, p_message):
        p_logmsg += '\tLast Will:\n'
        p_logmsg += p_message
        return p_logmsg

    def mqtt_dispatch(self, p_topic, p_message):
        """ This is the master dispatch table
        """
        l_logmsg = 'Dispatch\n\tTopic: {}\n'.format(p_topic)
        # Lwt can be from any device
        if p_topic[0] == 'lwt':
            l_logmsg += self._decodeLWT(l_logmsg, p_topic, p_message)
            return l_logmsg
        self.m_sender = self._get_field(p_message, 'Sender')
        self.m_name = self._get_field(p_message, 'Name')
        self.m_room_name = self._get_field(p_message, 'RoomName')
        l_logmsg += '\tSender: {}\n'.format(self.m_sender)
        if p_topic[0] == 'computer':
            l_logmsg = self.m_pyhouse_obj.APIs.Computer.ComputerAPI.DecodeMqtt(l_logmsg, p_topic, p_message)
        elif p_topic[0] == 'entertainment':
            l_logmsg = entertainmentMqtt(self.m_pyhouse_obj).decode(l_logmsg, p_topic, p_message)
        elif p_topic[0] == 'hvac':
            l_logmsg = self._decode_hvac(l_logmsg, p_topic, p_message)
        elif p_topic[0] == 'lighting':
            l_logmsg = self._decode_lighting(l_logmsg, p_topic, p_message)
        elif p_topic[0] == 'house':
            l_logmsg = self.m_pyhouse_obj.APIs.House.HouseAPI.DecodeMqtt(l_logmsg, p_topic, p_message)
        elif p_topic[0] == 'schedule':
            l_logmsg = self._decode_schedule(l_logmsg, p_topic, p_message)
        elif p_topic[0] == 'security':
            l_logmsg = securityMqtt(self.m_pyhouse_obj).decode(l_logmsg, p_topic, p_message)
        elif p_topic[0] == 'weather':
            l_logmsg = self._decode_weather(l_logmsg, p_topic, p_message)
        else:
            l_logmsg += 'OTHER: Unknown'
            l_logmsg += '\tMessage: {}\n'.format(PrettyFormatAny.form(p_message, 'Message', 160))
        return l_logmsg

#  ## END DBK
