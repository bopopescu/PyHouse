"""
@name: PyHouse/src/housing/test/test_internet.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 8, 2013
@summary: Test handling the internet information for a house.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Core.data_objects import PyHouseData, HousesData, HouseData, RoomData
from Modules.housing import internet
from test import xml_data
from Modules.web import web_utils
from Modules.utils.xml_tools import prettify

XML = xml_data.XML_LONG


class Test_02_XML(unittest.TestCase):

    def _pyHouses(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.HousesData[0] = HousesData()
        self.m_pyhouses_obj.HousesData[0].HouseObject = HouseData()
        self.m_pyhouses_obj.XmlRoot = self.m_root = ET.fromstring(XML)
        self.m_houses = self.m_root.find('Houses')
        self.m_house = self.m_houses.find('House')  # First house
        self.m_rooms = self.m_house.find('Rooms')
        self.m_room = self.m_rooms.find('Room')  # First room
        self.m_house_obj = HouseData()
        self.m_room_obj = RoomData()
        self.m_api = rooms.ReadWriteConfig()

    def setUp(self):
        self._pyHouses()

    def test_0201_buildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouses_obj.HousesData[0].HouseObject.Rooms, {}, 'No Rooms{}')

    def test_0202_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_houses.tag, 'Houses', 'XML - No Houses section')
        self.assertEqual(self.m_house.tag, 'House', 'XML - No House section')
        self.assertEqual(self.m_rooms.tag, 'Rooms', 'XML - No Rooms section')

    def test_0211_ReadOneRoomXml(self):
        """ Read in the xml file and fill in the first room's dict
        """
        l_room = self.m_api.read_one_room(self.m_room)
        self.assertEqual(l_room.Name, 'Test Living Room', 'Bad Name')
        self.assertEqual(l_room.Key, 0, 'Bad Key')
        self.assertEqual(l_room.Active, True, 'Bad Active')
        self.assertEqual(l_room.UUID, '12341234-1003-11e3-82b3-082e5f8cdfd2', 'Bad UUID')
        self.assertEqual(l_room.Comment, 'Test Comment', 'Bad Comment')
        self.assertEqual(l_room.Corner, '0.50, 10.50', 'Bad Corner')
        self.assertEqual(l_room.Size, '14.00, 13.50', 'Bad Size')
        # print('Room: {0:}'.format(vars(l_room)))

    def test_0212_ReadAllRoomsXml(self):
        """ Read in the xml file and fill in the rooms dict
        """
        l_rooms = self.m_api.read_rooms_xml(self.m_house)
        self.assertEqual(l_rooms[0].Name, 'Test Living Room', 'Bad Room')

    def test_0221_WriteOneRoomXml(self):
        """ Write out the XML file for the location section
        """
        l_room = self.m_api.read_one_room(self.m_house)
        l_xml = self.m_api.write_one_room(l_room)
        print('XML: {0:}'.format(prettify(l_xml)))


    def test_0222_WriteAllRoomsXml(self):
        """ Write out the XML file for the location section
        """
        l_rooms = self.m_api.read_rooms_xml(self.m_house)
        l_xml = self.m_api.write_rooms_xml(l_rooms)
        print('XML: {0:}'.format(prettify(l_xml)))


    def test_0231_CreateJson(self):
        """ Create a JSON object for Rooms.
        """
        self.m_pyhouses_obj.HousesData[0].HouseObject.Rooms = l_rooms = self.m_api.read_rooms_xml(self.m_house)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_rooms))
        print('JSON: {0:}'.format(l_json))

# ## END DBK
