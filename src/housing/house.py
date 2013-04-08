#!/usr/bin/python

"""Handle all the house(s) information.

main/house.py

There is one instance of this module for each house being controlled.

House.py knows everything about a single house.

There is location information for the house.  This is for calculating the
time of sunrise and sunset.  Additional calculations may be added such as
moonrise, tides, etc.

"""

# Import system type stuff
import logging
import xml.etree.ElementTree as ET

# Import PyMh files
from scheduling import schedule
from housing import internet
from utils import xml_tools

g_debug = 0
m_logger = None

Singletons = {}
House_Data = {}


class LocationData(object):

    def __init__(self):
        self.Active = True
        self.City = ''
        self.Key = 0
        self.Latitude = 0.0
        self.Longitude = 0.0
        self.Name = ''
        self.Phone = ''
        self.SavingTime = 0.0
        self.State = ''
        self.Street = ''
        self.TimeZone = 0.0
        self.ZipCode = ''

    def __str__(self):
        l_ret = ' Location:: '
        l_ret += 'Addr:{0:} {1:} {2:} {3:}, '.format(self.Street, self.City, self.State, self.ZipCode)
        l_ret += 'Lat:{0:}, Lon:{1:}'.format(self.Latitude, self.Longitude)
        return l_ret

    def get_active(self):
        return self.__Active
    def get_city(self):
        return self.__City
    def get_latitude(self):
        return self.__Latitude
    def get_longitude(self):
        return self.__Longitude
    def get_name(self):
        return self.__Name
    def get_phone(self):
        return self.__Phone
    def get_saving_time(self):
        return self.__SavingTime
    def get_state(self):
        return self.__State
    def get_street(self):
        return self.__Street
    def get_time_zone(self):
        return self.__TimeZone
    def get_zip_code(self):
        return self.__ZipCode

    def set_active(self, value):
        self.__Active = value
    def set_city(self, value):
        self.__City = value
    def set_latitude(self, value):
        self.__Latitude = value
    def set_longitude(self, value):
        self.__Longitude = value
    def set_name(self, value):
        self.__Name = value
    def set_phone(self, value):
        self.__Phone = value
    def set_saving_time(self, value):
        self.__SavingTime = value
    def set_state(self, value):
        self.__State = value
    def set_street(self, value):
        self.__Street = value
    def set_time_zone(self, value):
        self.__TimeZone = value
    def set_zip_code(self, value):
        self.__ZipCode = value

    Active = property(get_active, set_active, None, None)
    City = property(get_city, set_city, None, None)
    Latitude = property(get_latitude, set_latitude, None, None)
    Longitude = property(get_longitude, set_longitude, None, None)
    Name = property(get_name, set_name, None, None)
    Phone = property(get_phone, set_phone, None, None)
    SavingTime = property(get_saving_time, set_saving_time, None, "Minutes offset from standard time Eastern is +60")
    State = property(get_state, set_state, None, None)
    Street = property(get_street, set_street, None, None)
    TimeZone = property(get_time_zone, set_time_zone, None, None)
    ZipCode = property(get_zip_code, set_zip_code, None, None)


class RoomData(object):

    def __init__(self):
        self.Active = False
        self.Comment = ''
        self.Corner = ''
        self.HouseName = ''
        self.Key = 0
        self.Name = ''
        self.Size = ''

    def __str__(self):
        l_ret = ' Room:: Name:{0:} \t Size:{1:} \t Corner:{2:}\n'.format(self.get_name(), self.get_size(), self.get_corner())
        return l_ret

    def get_active(self):
        return self.__Active
    def get_comment(self):
        return self.__Comment
    def get_corner(self):
        return self.__Corner
    def get_house_name(self):
        return self.__HouseName
    def get_name(self):
        return self.__Name
    def get_size(self):
        return self.__Size
    def set_active(self, value):
        self.__Active = value
    def set_comment(self, value):
        self.__Comment = value
    def set_corner(self, value):
        self.__Corner = value
    def set_house_name(self, value):
        self.__HouseName = value
    def set_name(self, value):
        self.__Name = value
    def set_size(self, value):
        self.__Size = value

    Active = property(get_active, set_active, None, None)
    Comment = property(get_comment, set_comment, None, None)
    Corner = property(get_corner, set_corner, None, None)
    HouseName = property(get_house_name, set_house_name, None, None)
    Name = property(get_name, set_name, None, None)
    Size = property(get_size, set_size, None, None)


class HouseData(LocationData, RoomData):

    def __init__(self):
        self.Active = False
        self.Key = 0
        self.Name = ''
        self.MasterHouseNumber = 0
        self.InternetAPI = None
        self.LightingAPI = None
        self.ScheduleAPI = None
        self.Buttons = {}
        self.Controllers = {}
        self.Internet = {}
        self.Lights = {}
        self.Location = LocationData()
        self.Rooms = {}
        self.Schedule = {}

    def __str__(self):
        l_ret = ' House:: Name :{0:}, Active:{1:}, Key:{2:}'.format(self.Name, self.Active, self.Key)
        return l_ret


class HouseReadWriteConfig(xml_tools.ConfigTools, HouseData):
    """Use the internal data to read / write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    def read_location(self, p_house_obj, p_house_xml):
        if g_debug > 7:
            print "house.read_location()"
        l_location_obj = LocationData()
        if g_debug > 4:
            print "house.read_location() - Active=", l_location_obj.Active, l_location_obj.Name
        l_location_xml = p_house_xml.find('Location')
        l_location_obj.Street = self.get_text(l_location_xml, 'Street')
        l_location_obj.City = self.get_text(l_location_xml, 'City')
        l_location_obj.State = self.get_text(l_location_xml, 'State')
        l_location_obj.ZipCode = self.get_text(l_location_xml, 'ZipCode')
        l_location_obj.Phone = self.get_text(l_location_xml, 'Phone')
        l_location_obj.Latitude = self.get_float(l_location_xml, 'Latitude')
        l_location_obj.Longitude = self.get_float(l_location_xml, 'Longitude')
        l_location_obj.TimeZone = self.get_float(l_location_xml, 'TimeZone')
        l_location_obj.SavingTime = self.get_float(l_location_xml, 'SavingTime')
        p_house_obj.Location = l_location_obj
        if g_debug > 4:
            print "house.read_location()  loaded location for {0:}".format(p_house_obj.Name)

    def read_rooms(self, p_house_obj, p_house_xml):
        if g_debug > 7:
            print "house.read_rooms()"
        l_count = 0
        l_rooms = p_house_xml.find('Rooms')
        l_list = l_rooms.iterfind('Room')
        for l_room_xml in l_list:
            l_room_obj = RoomData()
            self.xml_read_common_info(l_room_obj, l_room_xml)
            l_room_obj.Key = l_count
            l_room_obj.HouseName = p_house_obj.Name
            l_room_obj.Comment = self.get_text(l_room_xml, 'Comment')
            l_room_obj.Corner = l_room_xml.findtext('Corner')
            l_room_obj.HouseName = l_room_xml.findtext('HouseName')
            l_room_obj.Size = l_room_xml.findtext('Size')
            p_house_obj.Rooms[l_count] = l_room_obj
            l_count += 1
            if g_debug > 6:
                print "house.read_rooms()   Name:{0:}, Active:{1:}, Key:{2:}".format(l_room_obj.Name, l_room_obj.Active, l_room_obj.Key)
        if g_debug > 4:
            print "house.read_rooms()  loaded {0:} rooms".format(l_count)

    def read_house(self, p_house_obj, p_house_xml):
        """Read house information, location and rooms.

        The main data is House_Data.
        """
        self.xml_read_common_info(p_house_obj, p_house_xml)
        self.get_int(p_house_xml, 'MasterHouseNumber')
        self.read_location(p_house_obj, p_house_xml)
        self.read_rooms(p_house_obj, p_house_xml)
        House_Data[0] = p_house_obj
        if g_debug > 1:
            print "house.read_house() - Loading XML data for House:{0:}".format(p_house_obj.Name)
        return House_Data

    def write_location(self, p_location_obj):
        """Replace the data in the 'House/Location' section with the current data.
        """
        l_entry = ET.Element('Location')
        ET.SubElement(l_entry, 'Street').text = p_location_obj.Street
        ET.SubElement(l_entry, 'City').text = p_location_obj.City
        ET.SubElement(l_entry, 'State').text = p_location_obj.State
        ET.SubElement(l_entry, 'ZipCode').text = p_location_obj.ZipCode
        ET.SubElement(l_entry, 'Phone').text = p_location_obj.Phone
        ET.SubElement(l_entry, 'Latitude').text = str(p_location_obj.Latitude)
        ET.SubElement(l_entry, 'Longitude').text = str(p_location_obj.Longitude)
        ET.SubElement(l_entry, 'TimeZone').text = str(p_location_obj.TimeZone)
        ET.SubElement(l_entry, 'SavingTime').text = str(p_location_obj.SavingTime)
        if g_debug > 2:
            print "house.write_location()"
        return l_entry

    def write_rooms(self, p_dict):
        l_count = 0
        l_rooms_xml = ET.Element('Rooms')
        for l_room_obj in p_dict.itervalues():
            l_entry = self.xml_create_common_element('Room', l_room_obj)
            ET.SubElement(l_entry, 'Comment').text = l_room_obj.Comment
            ET.SubElement(l_entry, 'Corner').text = l_room_obj.Corner
            ET.SubElement(l_entry, 'HouseName').text = l_room_obj.HouseName
            ET.SubElement(l_entry, 'Size').text = l_room_obj.Size
            l_rooms_xml.append(l_entry)
            l_count += 1
        if g_debug > 2:
            print "house.write_rooms() - Wrote {0:} rooms".format(l_count)
        return l_rooms_xml

    def write_house(self, p_house_obj):
        """Replace the data in the 'Houses' section with the current data.
        """
        l_house_xml = self.xml_create_common_element('House', p_house_obj)
        # ET.SubElement(l_house_xml, 'MasterHouseNumber').text = p_house_obj.MasterHouseNumber
        l_house_xml.append(self.write_location(p_house_obj.Location))
        l_house_xml.append(self.write_rooms(p_house_obj.Rooms))
        if g_debug > 2:
            print "house.write_house() - Name:{0:}, Key:{1:}".format(p_house_obj.Name, p_house_obj.Key)
        return l_house_xml


class LoadSaveAPI(HouseReadWriteConfig):
    """
    """

    def get_house_obj(self):
        return self.m_house_obj


class API(LoadSaveAPI):
    """
    """

    m_house_obj = HouseData()

    def __init__(self):
        """Create a house object for when we add a new house.
        """
        if g_debug >= 1:
            print "house.API.__init__()"
        self.m_logger = logging.getLogger('PyHouse.House')
        self.m_house_obj = HouseData()
        self.m_house_obj.ScheduleAPI = schedule.API(self.m_house_obj)

    def Start(self, _p_houses_obj, p_house_xml):
        """Start processing for all things house.
        May be stopped and then started anew to force reloading info.
        """
        self.read_house(self.m_house_obj, p_house_xml)
        if g_debug >= 1:
            print "house.API.Start() - House:{0:}, Active:{1:}".format(self.m_house_obj.Name, self.m_house_obj.Active)
        self.m_logger.info("Starting House {0:}.".format(self.m_house_obj.Name))
        self.m_house_obj.InternetAPI = internet.API(self.m_house_obj, p_house_xml)
        self.m_house_obj.ScheduleAPI.Start(self.m_house_obj, p_house_xml)
        self.m_house_obj.InternetAPI.Start()
        if g_debug >= 1:
            print "house.API.Start() has found -  Rooms:{0:}, Schedule:{1:}, Lights:{2:}, Controllers:{3:}".format(
                    len(self.m_house_obj.Rooms), len(self.m_house_obj.Schedule), len(self.m_house_obj.Lights), len(self.m_house_obj.Controllers))
        self.m_logger.info("Started.")
        return self.m_house_obj


    def Stop(self, p_xml):
        """Stop all houses.
        Return a filled in XML for the house.
        """
        if g_debug >= 1:
            print "\nhouse.Stop() - House:{0:}".format(self.m_house_obj.Name)
        self.m_logger.info("Stopping House:{0:}.".format(self.m_house_obj.Name))
        l_house_xml = self.write_house(self.m_house_obj)
        l_house_xml.extend(self.m_house_obj.ScheduleAPI.Stop(l_house_xml))
        l_house_xml.append(self.m_house_obj.InternetAPI.Stop())
        self.m_logger.info("Stopped.")
        if g_debug >= 1:
            print "house.Stop() - Name:{0:}, Count:{1:}".format(self.m_house_obj.Name, len(l_house_xml))
        return l_house_xml

    def SpecialTest(self):
        if g_debug > 0:
            print "house.API.SpecialTest()"
        self.m_house_obj.ScheduleAPI.SpecialTest()

# ##  END
