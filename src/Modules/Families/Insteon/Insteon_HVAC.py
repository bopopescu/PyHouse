"""
-*- test-case-name: PyHouse.src.Modules.Families.Insteon.test.test_Insteon_HVAC -*-

@name:      PyHouse/src/Modules/Families/Insteon/Insteon_HVAC.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2015 by D. Brian Kimmel
@note:      Created on Feb 18, 2010  Split into separate file Jul 9, 2014
@license:   MIT License
@summary:   This module decodes Insteon PLM response messages

Insteon HVAC module.

Adds HVAC (Heating Ventilation Air Conditioning) to the Insteon suite.
Specifically developed for the Venstar 1-day programmable digital thermostat.
This contains an Insteon radio modem.

Models 2491T1E and 2491T7E = (2491TxE)

see: 2441xxx pdf guides

"""



class Util(object):
    """
    """

    def get_device_obj(self, p_pyhouse_obj, p_address):
        l_ret = self._find_addr(p_pyhouse_obj.House.DeviceOBJs.Thermostats, p_address)
        return l_ret



class ihvac_utility(object):

    def decode_50_record(self, p_device_obj, p_controller_obj):
        """
        @param p_obj: is the Device (light, thermostat...) we are decoding.
        @param p_cmd1: is the Command 1 field in the message we are decoding.
        @param p_cmd2: is the Command 2 field in the message we are decoding.
        """
        l_mqtt_message = "Thermostat: "
        l_message = p_controller_obj._Message
        l_cmd1 = l_message[9]
        l_cmd2 = l_message[10]
        l_mqtt_message += ' Command1: {:#X},  Command2:{:#X}({:d})'.format(l_cmd1, l_cmd2, l_cmd2)
        if l_cmd1 == 0x01:
            l_mqtt_message += " Set Mode; "
        if l_cmd1 == 0x11:
            l_mqtt_message += " On; "
        if l_cmd1 == 0x13:
            l_mqtt_message += " Off; "
        if l_cmd1 == 0x6e:
            l_mqtt_message += ' temp = {}; '.format(l_cmd2)
        self.m_pyhouse_obj.APIs.Comp.MqttAPI.MqttPublish("pyhouse/thermostat/{}/info".format(p_device_obj.Name), l_mqtt_message)
        return

# ## END DBK
