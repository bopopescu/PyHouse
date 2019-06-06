"""
@name:      PyHouse/src/Housing/test/test_rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Test handling the rooms information for a house.

Passed all 18 tests - DBK 2018-02-13

"""
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2019-06-06'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.rooms import Api as roomsApi, Maint as roomsMaint
from Modules.Core.Utilities import json_tools
from Modules.Housing.test.xml_rooms import \
    TESTING_ROOM_NAME_0, \
    TESTING_ROOM_COMMENT_0, \
    TESTING_ROOM_CORNER_0, \
    TESTING_ROOM_SIZE_0, \
    TESTING_ROOM_ACTIVE_0, \
    TESTING_ROOM_KEY_0, \
    TESTING_ROOM_NAME_1, \
    TESTING_ROOM_FLOOR_0, \
    TESTING_ROOM_TYPE_0, \
    TESTING_ROOM_UUID_0, \
    TESTING_ROOM_NAME_2, \
    TESTING_ROOM_NAME_3, \
    TESTING_ROOM_CORNER_X_0, \
    TESTING_ROOM_SIZE_X_0, \
    TESTING_ROOM_KEY_3, \
    TESTING_ROOM_ACTIVE_3, \
    TESTING_ROOM_COMMENT_3, \
    TESTING_ROOM_UUID_3, \
    TESTING_ROOM_FLOOR_3, \
    TESTING_ROOM_SIZE_3, \
    TESTING_ROOM_TYPE_3, \
    TESTING_ROOM_CORNER_3, \
    TESTING_ROOM_UUID_2, \
    TESTING_ROOM_UUID_1, \
    TESTING_ROOM_LAST_UPDATE_0, \
    TESTING_ROOM_KEY_1, \
    TESTING_ROOM_ACTIVE_1, \
    TESTING_ROOM_COMMENT_1, \
    TESTING_ROOM_CORNER_1, \
    TESTING_ROOM_FLOOR_1, \
    TESTING_ROOM_LAST_UPDATE_1, \
    TESTING_ROOM_SIZE_1, \
    TESTING_ROOM_TYPE_1, \
    TESTING_ROOM_KEY_2, \
    TESTING_ROOM_ACTIVE_2, \
    TESTING_ROOM_COMMENT_2, \
    TESTING_ROOM_CORNER_2, \
    TESTING_ROOM_FLOOR_2, \
    TESTING_ROOM_LAST_UPDATE_2, \
    TESTING_ROOM_SIZE_2, \
    TESTING_ROOM_TYPE_2, \
    TESTING_ROOM_LAST_UPDATE_3
from Modules.Housing.test.xml_housing import \
    TESTING_HOUSE_NAME, \
    TESTING_HOUSE_ACTIVE, \
    TESTING_HOUSE_KEY, \
    TESTING_HOUSE_UUID, \
    TESTING_HOUSE_DIVISION
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

JSON = {
        'Name': TESTING_ROOM_NAME_3,
        'Key': TESTING_ROOM_KEY_3,
        'Active': TESTING_ROOM_ACTIVE_3,
        'UUID': TESTING_ROOM_UUID_3,
        'Comment': TESTING_ROOM_COMMENT_3,
        'Corner': TESTING_ROOM_CORNER_3,
        'Floor': TESTING_ROOM_FLOOR_3,
        'Size': TESTING_ROOM_SIZE_3,
        'RoomType': TESTING_ROOM_TYPE_3,
        'Add': True,
        'Delete': False
        }


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = roomsApi
        self.m_maint = roomsMaint


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_rooms')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, {})

    def test_02_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.room_sect.tag, 'RoomSection')
        self.assertEqual(self.m_xml.room.tag, 'Room')


class A2_XML(SetupMixin, unittest.TestCase):
    """ Now we test that the xml_xxxxx have set up the XML_LONG tree properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_HouseDiv(self):
        """ Test
        """
        l_xml = self.m_xml.house_div
        # print(PrettyFormatAny.form(l_xml, 'House'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_HOUSE_NAME)
        self.assertEqual(l_xml.attrib['Active'], TESTING_HOUSE_ACTIVE)
        self.assertEqual(l_xml.attrib['Key'], TESTING_HOUSE_KEY)
        self.assertEqual(l_xml.find('UUID').text, TESTING_HOUSE_UUID)

    def test_02_RoomCount(self):
        """ Test
        """
        l_xml = self.m_xml.room_sect
        # print(PrettyFormatAny.form(l_xml, 'Rooms'))
        self.assertEqual(len(l_xml), 4)
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_ROOM_NAME_0)
        self.assertEqual(l_xml[1].attrib['Name'], TESTING_ROOM_NAME_1)
        self.assertEqual(l_xml[2].attrib['Name'], TESTING_ROOM_NAME_2)
        self.assertEqual(l_xml[3].attrib['Name'], TESTING_ROOM_NAME_3)

    def test_03_Room0(self):
        """ Be sure that the XML contains everything in RoomInformation().
        """
        l_xml = self.m_xml.room
        # print(PrettyFormatAny.form(self.m_xml.room, 'Room'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ROOM_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ROOM_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ROOM_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_ROOM_UUID_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_ROOM_COMMENT_0)
        self.assertEqual(l_xml.find('Corner').text, TESTING_ROOM_CORNER_0)
        self.assertEqual(l_xml.find('Floor').text, TESTING_ROOM_FLOOR_0)
        self.assertEqual(l_xml.find('LastUpdate').text, str(TESTING_ROOM_LAST_UPDATE_0))
        self.assertEqual(l_xml.find('Size').text, TESTING_ROOM_SIZE_0)
        self.assertEqual(l_xml.find('RoomType').text, TESTING_ROOM_TYPE_0)

    def test_04_Room1(self):
        """ Be sure that the XML contains everything in RoomInformation().
        """
        l_xml = self.m_xml.room_sect[1]
        # print(PrettyFormatAny.form(l_xml, 'A2-04-A - Room'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ROOM_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ROOM_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ROOM_ACTIVE_1)
        self.assertEqual(l_xml.find('UUID').text, TESTING_ROOM_UUID_1)
        self.assertEqual(l_xml.find('Comment').text, TESTING_ROOM_COMMENT_1)
        self.assertEqual(l_xml.find('Corner').text, TESTING_ROOM_CORNER_1)
        self.assertEqual(l_xml.find('Floor').text, TESTING_ROOM_FLOOR_1)
        self.assertEqual(l_xml.find('LastUpdate').text, str(TESTING_ROOM_LAST_UPDATE_1))
        self.assertEqual(l_xml.find('Size').text, TESTING_ROOM_SIZE_1)
        self.assertEqual(l_xml.find('RoomType').text, TESTING_ROOM_TYPE_1)

    def test_05_Room2(self):
        """ Be sure that the XML contains everything in RoomInformation().
        """
        l_xml = self.m_xml.room_sect[2]
        # print(PrettyFormatAny.form(l_xml, 'A2-04-A - Room'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ROOM_NAME_2)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ROOM_KEY_2)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ROOM_ACTIVE_2)
        self.assertEqual(l_xml.find('UUID').text, TESTING_ROOM_UUID_2)
        self.assertEqual(l_xml.find('Comment').text, TESTING_ROOM_COMMENT_2)
        self.assertEqual(l_xml.find('Corner').text, TESTING_ROOM_CORNER_2)
        self.assertEqual(l_xml.find('Floor').text, TESTING_ROOM_FLOOR_2)
        self.assertEqual(l_xml.find('LastUpdate').text, str(TESTING_ROOM_LAST_UPDATE_2))
        self.assertEqual(l_xml.find('Size').text, TESTING_ROOM_SIZE_2)
        self.assertEqual(l_xml.find('RoomType').text, TESTING_ROOM_TYPE_2)

    def test_06_Room3(self):
        """ Be sure that the XML contains everything in RoomInformation().
        """
        l_xml = self.m_xml.room_sect[3]
        # print(PrettyFormatAny.form(l_xml, 'A2-04-A - Room'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ROOM_NAME_3)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ROOM_KEY_3)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ROOM_ACTIVE_3)
        self.assertEqual(l_xml.find('UUID').text, TESTING_ROOM_UUID_3)
        self.assertEqual(l_xml.find('Comment').text, TESTING_ROOM_COMMENT_3)
        self.assertEqual(l_xml.find('Corner').text, TESTING_ROOM_CORNER_3)
        self.assertEqual(l_xml.find('Floor').text, TESTING_ROOM_FLOOR_3)
        self.assertEqual(l_xml.find('LastUpdate').text, str(TESTING_ROOM_LAST_UPDATE_3))
        self.assertEqual(l_xml.find('Size').text, TESTING_ROOM_SIZE_3)
        self.assertEqual(l_xml.find('RoomType').text, TESTING_ROOM_TYPE_3)


class B1_Read(SetupMixin, unittest.TestCase):
    """ Test that we read in the XML config fproperly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneRoom(self):
        """ Read the xml and fill in the first room's dict
        """
        l_room = self.m_api._read_one_room(self.m_xml.room)
        # print(PrettyFormatAny.form(l_room, 'B1-1-A - One Room'))
        self.assertEqual(l_room.Name, TESTING_ROOM_NAME_0)
        self.assertEqual(l_room.Key, int(TESTING_ROOM_KEY_0))
        self.assertEqual(l_room.Active, bool(TESTING_ROOM_ACTIVE_0))
        self.assertEqual(l_room.UUID, TESTING_ROOM_UUID_0)
        #
        self.assertEqual(l_room.Comment, TESTING_ROOM_COMMENT_0)
        self.assertEqual(l_room.Corner.X_Easting, float(TESTING_ROOM_CORNER_X_0))
        self.assertEqual(l_room.Floor, TESTING_ROOM_FLOOR_0)
        self.assertEqual(l_room.LastUpdate, TESTING_ROOM_LAST_UPDATE_0)
        self.assertEqual(l_room.Size.X_Easting, float(TESTING_ROOM_SIZE_X_0))
        self.assertEqual(l_room.RoomType, TESTING_ROOM_TYPE_0)

    def test_2_AllRooms(self):
        """ Read in the xml file and fill in the rooms dict
        """
        l_rooms = self.m_api(self.m_pyhouse_obj).read_rooms_xml(self.m_pyhouse_obj)
        print(json_tools.encode_json(l_rooms[0]))
        print(PrettyFormatAny.form(l_rooms, 'B1-2-A - All Rooms'))
        # print(PrettyFormatAny.form(l_rooms[0], 'B1-2-A - All Rooms'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'B1-2-b - PyHouse_Obj'))
        self.assertEqual(len(l_rooms), 4)
        print(l_rooms[0].Name)
        self.assertEqual(l_rooms[0].Name, TESTING_ROOM_NAME_0)
        self.assertEqual(l_rooms[1].Name, TESTING_ROOM_NAME_1)
        self.assertEqual(l_rooms[2].Name, TESTING_ROOM_NAME_2)
        self.assertEqual(l_rooms[3].Name, TESTING_ROOM_NAME_3)


class B2_Write(SetupMixin, unittest.TestCase):
    """ Test that we write out the XML config properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneRoom(self):
        """ Write out the XML file for the location section
        """
        l_xml = self.m_xml.room
        # print(PrettyFormatAny.form(l_xml, 'B2-01-A - Room Xml'))
        l_room = self.m_api._read_one_room(l_xml)
        # print(PrettyFormatAny.form(l_room, 'B2-01-B - One Room'))
        l_xml = self.m_api.write_one_room(l_room)
        # print(PrettyFormatAny.form(l_xml, 'B2-01-C - One Room'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ROOM_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ROOM_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ROOM_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_ROOM_UUID_0)
        #
        self.assertEqual(l_xml.find('Comment').text, TESTING_ROOM_COMMENT_0)
        self.assertEqual(l_xml.find('Corner').text, TESTING_ROOM_CORNER_0)
        self.assertEqual(l_xml.find('Floor').text, TESTING_ROOM_FLOOR_0)
        self.assertEqual(l_xml.find('LastUpdate').text, str(TESTING_ROOM_LAST_UPDATE_0))
        self.assertEqual(l_xml.find('Size').text, TESTING_ROOM_SIZE_0)
        self.assertEqual(l_xml.find('RoomType').text, TESTING_ROOM_TYPE_0)

    def test_02_AllRooms(self):
        """ Write out the XML file for the location section
        """
        l_rooms = self.m_api(self.m_pyhouse_obj).read_rooms_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_rooms_xml(l_rooms)
        # print(PrettyFormatAny.form(l_xml, 'B2-02-A - All Rooms'))
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_ROOM_NAME_0)
        self.assertEqual(l_xml[1].attrib['Name'], TESTING_ROOM_NAME_1)
        self.assertEqual(l_xml[2].attrib['Name'], TESTING_ROOM_NAME_2)
        self.assertEqual(l_xml[3].attrib['Name'], TESTING_ROOM_NAME_3)


class D1_Maint(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def _print(self, p_rooms):
        # for l_obj in p_rooms.values():
        #    print('D1-Print - Key:{}; Name:{}; UUID:{}; Update:{};'.format(
        #            l_obj.Key, l_obj.Name, l_obj.UUID, l_obj.LastUpdate))
        # print
        pass

    def test_01_Extract(self):
        """ Test extracting information passed back by the browser.
        The data comes in JSON format..
        """
        l_obj = self.m_maint()._json_2_obj(JSON)
        # print(PrettyFormatAny.form(l_obj, 'D1-01-A - Json'))
        self.assertEqual(l_obj.Name, TESTING_ROOM_NAME_3)
        self.assertEqual(l_obj.Key, int(TESTING_ROOM_KEY_3))
        self.assertEqual(l_obj.Active, TESTING_ROOM_ACTIVE_3)
        self.assertEqual(l_obj.UUID, TESTING_ROOM_UUID_3)
        self.assertEqual(l_obj.Comment, TESTING_ROOM_COMMENT_3)
        # self.assertEqual(l_obj.Corner, TESTING_ROOM_CORNER_3)
        self.assertEqual(l_obj.Floor, TESTING_ROOM_FLOOR_3)
        # self.assertEqual(l_obj.Size, TESTING_ROOM_SIZE_3)
        self.assertEqual(l_obj.RoomType, TESTING_ROOM_TYPE_3)

    def test_02_Add(self):
        """
        """
        l_rooms = self.m_api(self.m_pyhouse_obj).read_rooms_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Rooms = l_rooms
        l_obj = self.m_maint()._json_2_obj(JSON)
        self._print(l_rooms)
        # print(PrettyFormatAny.form(l_obj, 'D1-02-A - Json'))
        l_rooms = self.m_maint()._add_change_room(self.m_pyhouse_obj, l_obj)
        self._print(l_rooms)


class E1_Json(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_CreateJson(self):
        """ Create a JSON object for Rooms.
        """
        self.m_pyhouse_obj.House.Rooms = l_rooms = self.m_api(self.m_pyhouse_obj).read_rooms_xml(self.m_pyhouse_obj)
        l_json = json_tools.encode_json(l_rooms)
        l_obj = json_tools.decode_json_unicode(l_json)
        # print(PrettyFormatAny.form(l_json, 'JSON', 80))
        # print(PrettyFormatAny.form(l_obj, 'JSON', 80))
        self.assertEqual(len(l_obj), len(l_rooms))


class F1_Match(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_ByName(self):
        """ Create a JSON object for Rooms.
        """
        l_search = TESTING_ROOM_NAME_1
        self.m_pyhouse_obj.House.Rooms = self.m_api(self.m_pyhouse_obj).read_rooms_xml(self.m_pyhouse_obj)
        l_obj = self.m_api(self.m_pyhouse_obj).find_room_name(self.m_pyhouse_obj, l_search)
        # print(PrettyFormatAny.form(l_obj, 'F1-01-A - Room - {}'.format(l_search)))
        self.assertEqual(l_obj.Name, TESTING_ROOM_NAME_1)
        self.assertEqual(l_obj.UUID, TESTING_ROOM_UUID_1)

    def test_02_ByUuid(self):
        """ Create a JSON object for Rooms.
        """
        l_search = TESTING_ROOM_UUID_2
        self.m_pyhouse_obj.House.Rooms = self.m_api(self.m_pyhouse_obj).read_rooms_xml(self.m_pyhouse_obj)
        l_obj = self.m_api(self.m_pyhouse_obj).find_room_uuid(self.m_pyhouse_obj, l_search)
        # print(PrettyFormatAny.form(l_obj, 'F1-02-A - Room - {}'.format(l_search)))
        self.assertEqual(l_obj.Name, TESTING_ROOM_NAME_2)
        self.assertEqual(l_obj.UUID, TESTING_ROOM_UUID_2)


class Y1_Yaml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_ByName(self):
        """ Create a JSON object for Rooms.
        """
        l_yaml = self.m_api(self.m_pyhouse_obj)._read_yaml()
        print(PrettyFormatAny.form(l_yaml, 'Y1-01-A'))
        print(PrettyFormatAny.form(l_yaml['Floors'], 'Y1-01-B'))
        print(PrettyFormatAny.form(l_yaml['Rooms'], 'Y1-01-C'))
        self.assertEqual(l_yaml['Rooms'][0]['Name'], 'Outside')
        # self.assertEqual(l_yaml.UUID, TESTING_ROOM_UUID_1)

# ## END DBK
