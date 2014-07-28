"""
@name: PyHouse/src/Modules/drivers/test/test_Driver_Serial.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013_2014 by D. Brian Kimmel
@license: MIT License
@note: Created on May 4, 2013
@summary: This module is for testing local node data.

Passed 3 XML tests - DBK - 2014-07-27
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData
from Modules.drivers import Driver_Serial
from Modules.lights import lighting_controllers
from Modules.families import family
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.utils.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self, self.m_root_xml)
        SetupPyHouseObj().BuildXml(self.m_root_xml)
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_api = Driver_Serial.API()
        self.m_controller_obj = ControllerData()

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouseData')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection', 'XML - No Controllers section')
        self.assertEqual(self.m_xml.controller.tag, 'Controller', 'XML - No Controller section')

    def test_0221_ReadSerialXml(self):
        l_interface = self.m_api._read_serial_interface_xml(self.m_controller_obj, self.m_xml.controller)
        self.assertEqual(l_interface.BaudRate, 19200, 'Bad Baud Rate')
        PrettyPrintAny(l_interface, 'Read Interface', 100)

    def test_0241_WriteSerialXml(self):
        l_obj = lighting_controllers.ControllersAPI(self.m_pyhouse_obj).read_one_controller_xml(self.m_xml.controller)
        PrettyPrintAny(l_obj, 'Controller', 120)
        l_ret = self.m_api._write_serial_interface_xml(self.m_xml.controller, l_obj)
        PrettyPrintAny(l_ret, 'Interface Xml', 120)


# ## END
