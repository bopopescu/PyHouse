"""
@name:      PyHouse/src/Modules/families/Insteon/test/test_Insteon_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 27, 2013
@summary:   This module is for testing Insteon conversion routines.

Passed all 6 tests - DBK - 2016-09-19

"""
from Modules.Utilities.tools import PrintBytes

__updated__ = '2016-09-19'

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Families.Insteon.Insteon_utils import Util, Decode as utilDecode
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG
from Modules.Core.data_objects import ControllerData
from Modules.Utilities.debug_tools import PrettyFormatAny

ADDR_DR_SLAVE_MSG = bytearray(b'\x16\xc9\xd0')
ADDR_DR_SLAVE_INT = (((0x16 * 256) + 0xc9) * 256) + 0xd0  # 1493456
ADDR_NOOK_MSG = bytearray(b'\x17\xc2\x72')
ADDR_NOOK_INT = (((0x17 * 256) + 0xc2) * 256) + 0x72  #  1557106

MSG_50 = bytearray(b'\x02\x50\x16\xc9\xd0\x02\x04\x81\x27\x09\x00')
MSG_62 = bytearray(b'\x02\x62\x17\xc2\x72\x0f\x19\x00\x06')


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_obj = ControllerData()
        self.inst = Util


class A1_Conversions(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Message2int(self):
        """ Get 3 bytes and convert it ti a laww
        """
        result = self.inst.message2int(MSG_50[2:5])
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse'))
        self.assertEqual(result, ADDR_DR_SLAVE_INT)
        #
        result = self.inst.message2int(MSG_62[2:5])
        self.assertEqual(result, ADDR_NOOK_INT)


class C1_Conversions(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Message2int(self):
        """ Get 3 bytes and convert it ti a laww
        """
        result = self.inst.message2int(MSG_50[2:5])
        print(result)
        self.assertEqual(result, ADDR_DR_SLAVE_INT)
        #
        result = self.inst.message2int(MSG_62[2:5])
        self.assertEqual(result, ADDR_NOOK_INT)

    def test_02_Int2message(self):
        """ Convert a long int to a 3 byte address
        """
        l_msg = MSG_50
        result = self.inst.int2message(ADDR_DR_SLAVE_INT, l_msg, 2)
        print(PrintBytes(result))
        self.assertEqual(result[2:5], ADDR_DR_SLAVE_MSG)
        #
        l_msg = MSG_62
        result = self.inst.int2message(ADDR_NOOK_INT, l_msg, 2)
        self.assertEqual(result[2:5], ADDR_NOOK_MSG)

    def test_03_Json(self):
        pass


class D1_Decode(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Devcat(self):
        l_dev = b'\x02\x04'
        l_ret = utilDecode._devcat(l_dev, self.m_obj)
        print(PrettyFormatAny.form(l_ret, 'D1-01-A - xxx'))
        self.assertEqual(self.m_obj.DevCat, 0x0204)
        #
        l_dev = MSG_50
        # l_c = l_dev[5:7]
        # print(FormatBytes(l_c))
        l_ret = utilDecode._devcat(l_dev[5:7], self.m_obj)
        self.assertEqual(self.m_obj.DevCat, 0x0204)


class D2_Decode(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_02_GetObj(self):
        """
        """
        l_msg = MSG_50
        print(PrintBytes(l_msg), 'D2-01-A - Message')
        l_ret = utilDecode.get_obj_from_message(self.m_pyhouse_obj, l_msg)
        print(l_ret)
        print(PrettyFormatAny.form(l_ret, 'Combined Dicts'))

# ## END DBK
