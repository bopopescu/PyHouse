"""
@name:      PyHouse/src/Modules.Core.Utilities.test/test_json_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 25, 2015
@Summary:

Passed all 5 tests - DBK - 2017-01-20

"""
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2017-01-20'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities  import json_tools


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_json_tools')


class A1_Json(SetupMixin, unittest.TestCase):
    """
    This series tests the complex PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Encode(self):
        l_obj = self.m_pyhouse_obj.House.Location
        l_json = json_tools.encode_json(l_obj)
        print(l_json)
        PrettyFormatAny.form(l_json, "A1-01-A - Location")
        self.assertSubstring('State', l_json)
        self.assertSubstring('City', l_json)

    def test_02_Decode(self):
        l_json = json_tools.encode_json(self.m_pyhouse_obj.Computer)
        l_dict = json_tools.decode_json_unicode(l_json)
        print(l_dict)
        print(PrettyFormatAny.form(l_dict, 'A1-02-A - Decoded Info'))
        self.assertEqual(l_dict['Name'], self.m_pyhouse_obj.Computer.Name)


class A2_Decode(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Unicode(self):
        y = json_tools.convert_from_unicode(u'ABC')
        self.assertEquals(y, 'ABC')

    def test_02_Ascii(self):
        y = json_tools.convert_from_unicode('ABC')
        self.assertEquals(y, 'ABC')

# ## END DBK