"""
@name: PyHouse/src/test/test_mixin.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 40, 2013
@summary: Test handling the information for a house.

"""

# Import system type stuff

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, PyHouseAPIs, \
            CoreServicesInformation, \
            ComputerInformation, \
            HouseInformation, HouseObjs, \
            TwistedInformation, \
            XmlInformation
# from Modules.utils.tools import PrettyPrintAny


class XmlData(object):
    def __init__(self):
        self.root = None
        self.house_div = None
        self.button_sect = None
        self.button = None
        self.controller_sect = None
        self.controller = None
        self.light_sect = None
        self.light = None
        self.location_sect = None
        self.room_sect = None
        self.room = None
        self.schedule_sect = None
        self.schedule = None
        self.thermostat_sect = None
        self.thermostat = None
        #
        self.computer_div = None
        self.internet_sect = None
        self.log_sect = None
        self.node_sect = None
        self.web_sect = None


class SetupPyHouseObj(object):
    """
    """

    def _BuildHouse(self):
        l_ret = HouseInformation()
        l_ret.Name = 'Test House'
        l_ret.Active = True
        l_ret.Key = 0
        l_ret.OBJs = HouseObjs()
        return l_ret

    def BuildPyHouseObj(self, p_root):
        l_ret = PyHouseData()
        l_ret.APIs = PyHouseAPIs
        l_ret.Computer = ComputerInformation()
        l_ret.House = self._BuildHouse()
        l_ret.Services = CoreServicesInformation()
        l_ret.Twisted = TwistedInformation()
        l_ret.Xml = XmlInformation()
        l_ret.Xml.XmlRoot = p_root
        return l_ret

    def BuildXml(self, p_root_xml):
        l_xml = XmlData()
        l_xml.root = p_root_xml
        try:
            l_xml.house_div = p_root_xml.find('HouseDivision')
            #
            l_xml.button_sect = l_xml.house_div.find('ButtonSection')
            l_xml.controller_sect = l_xml.house_div.find('ControllerSection')
            l_xml.light_sect = l_xml.house_div.find('LightSection')
            l_xml.location_sect = l_xml.house_div.find('LocationSection')
            l_xml.room_sect = l_xml.house_div.find('RoomSection')
            l_xml.schedule_sect = l_xml.house_div.find('ScheduleSection')
            l_xml.thermostat_sect = l_xml.house_div.find('ThermostatSection')
            #
            l_xml.button = l_xml.button_sect.find('Button')
            l_xml.controller = l_xml.controller_sect.find('Controller')
            l_xml.light = l_xml.light_sect.find('Light')
            l_xml.room = l_xml.room_sect.find('Room')
            l_xml.schedule = l_xml.schedule_sect.find('Schedule')
            l_xml.thermostat = l_xml.thermostat_sect.find('Thermostat')
            #
            l_xml.computer_div = p_root_xml.find('ComputerDivision')
            l_xml.internet_sect = l_xml.computer_div.find('InternetSection')
            l_xml.log_sect = l_xml.computer_div.find('LogSection')
            l_xml.node_sect = l_xml.computer_div.find('InternetSection')
            l_xml.web_sect = l_xml.computer_div.find('WebSection')
        except AttributeError:
            pass
        # PrettyPrintAny(l_xml, 'TestMixin - Self', 100)
        return l_xml

    def setUp(self):
        self.BuildPyHouseObj()

# ## END DBK
