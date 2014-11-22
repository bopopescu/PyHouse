"""
-*- test-case-name: PyHouse.src.Modules.Housing.test.test_house -*-

@name: PyHouse/src/Modules/Housing/house.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 10, 2013
@summary: Handle all of the information for a house.

There is one instance of this module for each house being controlled.

House.py knows everything about a single house.

Rooms and lights and HVAC are associated with a particular house.
"""

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import HouseInformation, HouseObjs
from Modules.Families import family
from Modules.Scheduling import schedule, sunrisesunset
from Modules.Housing import location
from Modules.Housing import rooms
from Modules.Computer import logging_pyh as Logger
# from Modules.Utilities.tools import PrettyPrintAny

g_debug = 1
LOG = Logger.getLogger('PyHouse.House       ')


class HouseItems(object):
    """
    Process all the house based items:
        Location (1)
        Rooms (0+)
        Schedule (0+)
        Weather (1)

        Communication (0+)
        Entertainment (0+)
        HVAC (0+)
        Irrigation (0+)
        Lighting (0+)
        Pools (0+)
        Security (0+)
    """

    def init_all_components(self):
        self.m_house_obj.APIs.ScheduleAPI = schedule.API(self.m_house_obj)
        pass


class ReadWriteConfigXml(location.ReadWriteConfigXml, rooms.ReadWriteConfigXml):
    """Use the internal data to read / write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    def _get_house_xml(self, p_pyhouse_obj):
        l_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision')
        return l_xml

    def _read_base_house(self, p_pyhouse_obj):
        l_xml = self._get_house_xml(p_pyhouse_obj)
        self.read_base_object_xml(p_pyhouse_obj.House, l_xml)
        return l_xml

    def read_house_xml(self, p_pyhouse_obj):
        """Read house information, location and rooms.
        """
        l_xml = self._get_house_xml(p_pyhouse_obj)
        self.read_base_object_xml(p_pyhouse_obj.House, l_xml)
        p_pyhouse_obj.House.OBJs.Location = self.read_location_xml(l_xml)
        p_pyhouse_obj.House.OBJs.Rooms = self.read_rooms_xml(l_xml)
        return p_pyhouse_obj.House

    def write_house_xml(self, p_house_obj):
        """Replace the data in the 'Houses' section with the current data.
        """
        l_house_xml = self.write_base_object_xml('HouseDivision', p_house_obj)
        l_house_xml.append(self.write_location_xml(p_house_obj.OBJs.Location))
        l_house_xml.append(self.write_rooms_xml(p_house_obj.OBJs.Rooms))
        return l_house_xml


class Utility(ReadWriteConfigXml):
    """
    """

    m_pyhouse_obj = None

    def update_pyhouse_obj(self, p_pyhouse_obj):
        p_pyhouse_obj.House = HouseInformation()
        p_pyhouse_obj.House.OBJs = HouseObjs()
        return p_pyhouse_obj

    def add_api_references(self, p_pyhouse_obj):
        p_pyhouse_obj.APIs.HouseAPI = self
        p_pyhouse_obj.APIs.FamilyAPI = family.API()
        p_pyhouse_obj.APIs.SunRiseSetAPI = sunrisesunset.API()
        p_pyhouse_obj.APIs.ScheduleAPI = schedule.API()

    def start_house_parts(self, p_pyhouse_obj):
        p_pyhouse_obj.APIs.ScheduleAPI.Start(self.m_pyhouse_obj)

    def stop_house_parts(self):
        self.m_pyhouse_obj.APIs.ScheduleAPI.Stop()

    def get_sunrise_set(self, p_pyhouse_obj):
        """
        Retrieve datetime.datetime for sunrise and sunset.
        """
        p_pyhouse_obj.APIs.SunRiseSetAPI = sunrisesunset.API()
        p_pyhouse_obj.APIs.SunRiseSetAPI.Start(p_pyhouse_obj)
        p_pyhouse_obj.House.OBJs.Location._Sunrise = p_pyhouse_obj.APIs.SunRiseSetAPI.get_sunrise_datetime()
        p_pyhouse_obj.House.OBJs.Location._Sunset = p_pyhouse_obj.APIs.SunRiseSetAPI.get_sunset_datetime()


class API(Utility):
    """
    """

    def Start(self, p_pyhouse_obj):
        """Start processing for all things house.
        Read in the XML file and update the internal data.
        May be stopped and then started anew to force reloading info.
        """
        LOG.info("Starting.")
        self.update_pyhouse_obj(p_pyhouse_obj)
        self.add_api_references(p_pyhouse_obj)
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.House = self.read_house_xml(p_pyhouse_obj)
        p_pyhouse_obj.House.OBJs.FamilyData = p_pyhouse_obj.APIs.FamilyAPI.Start(p_pyhouse_obj)
        self.get_sunrise_set(p_pyhouse_obj)
        self.start_house_parts(p_pyhouse_obj)
        LOG.info("Started House {0:}".format(self.m_pyhouse_obj.House.Name))

    def Stop(self):
        """Stop all houses.
        Append the house XML to the passed in xlm tree.
        """
        LOG.info("Stopping House.")
        self.stop_house_parts()
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        """
        Take a snapshot of the current Configuration/Status and write out an XML file.
        """
        l_xml = self.write_house_xml(self.m_pyhouse_obj.House)
        self.m_pyhouse_obj.APIs.ScheduleAPI.WriteXml(l_xml)
        p_xml.append(l_xml)
        LOG.info("Wrote XML.")

# ##  END DBK
