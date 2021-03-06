"""
@name:      PyHouse/Project/src/_test/test_testing_mixin.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Oct 6, 2014
@Summary:

Passed all 16 tests - DBK - 2019-06-23

"""
from Modules.Core import PyHouseInformation
from Modules.Computer.computer import ComputerInformation
from Modules.House import HouseInformation

__updated__ = '2020-02-04'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin:

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()

    def setUpObj(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_testing_mixin')


class A1_Setup(SetupMixin, unittest.TestCase):
    """ This section tests the SetupMixin Class
    """

    def setUp(self):
        pass

    def test_01_BuildObjs(self):
        """ Be sure that the PyHouse obj is built correctly
        """
        l_obj = SetupPyHouseObj().BuildPyHouseObj()
        print(PrettyFormatAny.form(l_obj, 'A1-02-A - PyHouseObj', 90))
        self.assertIsInstance(l_obj, PyHouseInformation)
        self.assertIsInstance(l_obj.Computer, ComputerInformation)
        self.assertIsInstance(l_obj.House, HouseInformation)

    def test_03_YAML(self):
        """ Be sure that the YAML contains the right stuff.
        """
        l_obj = SetupPyHouseObj().BuildPyHouseObj()
        # print(PrettyFormatAny.form(l_obj, 'A1-03-A - PyHouseObj', 90))
        print(PrettyFormatAny.form(l_obj._Config, 'A1-03-B - _Config', 90))


class B1_Empty(SetupMixin, unittest.TestCase):
    """ This section tests the SetupMixin Class
    """

    def setUp(self):
        SetupMixin.setUpObj(self)
        pass

    def test_01_Obj(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'B1-01-A - PyHouse'))
        pass

    def test_02_Computer(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'B1-02-A - PyHouse.Computer'))
        pass

    def test_03_House(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'B1-03-A - PyHouse.House'))
        pass

    def test_04_Location(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Location, 'B1-04-A - PyHouse.House.Location'))
        pass


class B2_Long(SetupMixin, unittest.TestCase):
    """ This section tests the SetupMixin Class
    """

    def setUp(self):
        SetupMixin.setUpObj(self)
        pass

    def test_01_Obj(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'B2-01-A - PyHouse'))
        pass

    def test_02_Computer(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'B2-02-A - PyHouse.Computer'))
        pass

    def test_03_House(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'B2-03-A - PyHouse.House'))
        pass

    def test_04_Location(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Location, 'B2-04-A - PyHouse.House.Location'))
        pass


class C1_Build(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by inernet.
    """

    def setUp(self):
        self.m_api = SetupPyHouseObj()

    def test_01_Computer(self):
        l_config = self.m_api._build_computer()
        # print(PrettyFormatAny.form(l_config, 'C1-01-A - Config'))
        # self.assertDictEqual(l_config.Email, {})
        # self.assertDictEqual(l_config.InternetConnection, {})
        # self.assertDictEqual(l_config.Nodes, {})
        # self.assertDictEqual(l_config.Web, {})
        pass

# ## END DBK
