"""
@name: PyHouse/src/housing/test/test_rooms.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 10, 2013
@summary: Test handling the rooms information for a house.


Tests all working OK - DBK 2014-05-22
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Housing import rooms
from Modules.Web import web_utils
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_XML(SetupMixin, unittest.TestCase):

    def _pyHouses(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = rooms.ReadWriteConfigXml()

    def setUp(self):
        self._pyHouses()

    def test_0201_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouse_obj.House.OBJs.Rooms, {}, 'No Rooms{}')

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No Houses Division')
        self.assertEqual(self.m_xml.room_sect.tag, 'RoomSection', 'XML - No Rooms section')
        self.assertEqual(self.m_xml.room.tag, 'Room', 'XML - No Room')

    def test_0211_ReadOneRoom(self):
        """ Read in the xml file and fill in the first room's dict
        """
        l_room = self.m_api.read_one_room(self.m_xml.room)
        PrettyPrintAny(l_room, 'Room')
        self.assertEqual(l_room.Name, 'Master Bath', 'Bad Name')
        self.assertEqual(l_room.Key, 0, 'Bad Key')
        self.assertEqual(l_room.Active, True, 'Bad Active')
        self.assertEqual(l_room.Comment, 'Test Comment', 'Bad Comment')
        self.assertEqual(l_room.Corner, '0.50, 10.50', 'Bad Corner')
        self.assertEqual(l_room.Size, '14.00, 13.50', 'Bad Size')

    def test_0212_ReadAllRoomsXml(self):
        """ Read in the xml file and fill in the rooms dict
        """
        l_rooms = self.m_api.read_rooms_xml(self.m_xml.house_div)
        PrettyPrintAny(l_rooms, 'Rooms')
        self.assertEqual(l_rooms[0].Name, 'Master Bath', 'Bad Room')

    def test_0221_WriteOneRoomXml(self):
        """ Write out the XML file for the location section
        """
        l_room = self.m_api.read_one_room(self.m_xml.house_div)
        l_xml = self.m_api.write_one_room(l_room)
        PrettyPrintAny(l_xml, 'One Room', 120)


    def test_0222_WriteAllRoomsXml(self):
        """ Write out the XML file for the location section
        """
        l_rooms = self.m_api.read_rooms_xml(self.m_xml.house_div)
        l_xml = self.m_api.write_rooms_xml(l_rooms)
        PrettyPrintAny(l_xml, 'All Rooms', 120)


    def test_0231_CreateJson(self):
        """ Create a JSON object for Rooms.
        """
        self.m_pyhouse_obj.House.OBJs.Rooms = l_rooms = self.m_api.read_rooms_xml(self.m_xml.house_div)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_rooms))
        print('JSON: {0:}'.format(l_json))
        PrettyPrintAny(l_json, 'JSON', 120)

# ## END DBK
