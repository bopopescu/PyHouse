"""
@name:      PyHouse/src/Modules.Core.Utilities.test_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2013-2017 by D. Brian Kimmel
@note:      Created on Apr 11, 2013
@license:   MIT License
@summary:   Various functions and utility methods.

Passed all 3 tests - DBK - 2016-11-22

"""

__updated__ = '2019-10-06'

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

#  Import PyMh files
from Modules.Core.setup_logging import LOGGING_DICT
from Modules.Core.Utilities.obj_defs import GetPyhouse
from Modules.Core.Utilities import tools
from Modules.House.Lighting.lighting_lights import Api as lightsApi
from Modules.House.Family.family import Api as familyApi
from Modules.Core import logging_pyh as Logger
from _test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_version = '1.4.0'


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_tools')


class C1_Find(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = GetPyhouse(self.m_pyhouse_obj)
        self.m_light_api = lightsAPI()
        self.m_pyhouse_obj._Families = familyApi(self.m_pyhouse_obj).m_family
        self.m_pyhouse_obj.House.Lighting.Lights = self.m_light_api.read_all_lights_xml(self.m_pyhouse_obj)

    def test_01_Setup(self):
        l_loc = self.m_api.Location().Latitude
        #  print(l_loc)

#  ## END DBK
