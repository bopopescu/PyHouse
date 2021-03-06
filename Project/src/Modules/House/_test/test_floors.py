"""
@name:      Modules/House/_test/test_rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 28, 2019
@summary:   Test handling the rooms information for a house.

Passed all 10 tests - DBK 2019-06-28

"""
__updated__ = '2020-02-04'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.House import floors
from Modules.Core.Config.config_tools import Api as configApi
from Modules.House import HouseInformation
from Modules.Core.Config import config_tools

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML = """\
Floors:
   - Name: Outside
     Floor: 0
     Comment: Outside

   - Name: 1st
     Floor: 1
     Comment: The first floor

"""


class SetupMixin:

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_api = floors.Api(self.m_pyhouse_obj)
        self.m_config_api = configApi(self.m_pyhouse_obj)
        self.m_api._add_storage()
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title')  # so it is defined when printing is cleaned up.
        print('Id: test_floors')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly.
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-01-B - House'))
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Floors, 'A1-01-C - Floors'))
        self.assertEqual(self.m_pyhouse_obj.House.Floors.Floor, {})


class C1_YamlRead(SetupMixin, unittest.TestCase):
    """ Read the YAML config files.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_working_floors = self.m_pyhouse_obj.House.Floors

    def test_01_Build(self):
        """ The basic read info as set up
        """
        print(PrettyFormatAny.form(self.m_working_floors, 'C1-01-A - WorkingRooms'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'C1-01-B - House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Floors, 'C1-01-C - Floors'))

    def test_02_ReadFile(self):
        """ Read the rooms.yaml config file
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_config_file(self.m_filename)
        l_yaml = l_node.Yaml
        l_yamlfloors = l_yaml['Floors']
        print(PrettyFormatAny.form(l_node, 'C1-02-A - Node'))
        # print(PrettyFormatAny.form(l_yaml, 'C1-02-B - Yaml'))
        # print(PrettyFormatAny.form(l_yamlfloors, 'C1-02-C - YamlFloors'))
        # print(PrettyFormatAny.form(l_yamlfloors[0], 'C1-02-J - Floor-0'))
        # print(PrettyFormatAny.form(l_yamlfloors[3], 'C1-02-M - Floor-3'))
        self.assertEqual(l_yamlfloors[0]['Name'], 'Outside')
        self.assertEqual(l_yamlfloors[1]['Name'], 'Basement')
        self.assertEqual(l_yamlfloors[2]['Name'], '1st')
        self.assertEqual(l_yamlfloors[3]['Name'], '2nd')
        self.assertEqual(len(l_yamlfloors), 4)

    def test_03_ExtractFloor(self):
        """ Extract one room info from the yaml
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_config_file(self.m_filename)
        l_yamlfloors = l_node.Yaml['Floors'][2]
        l_obj = self.m_yaml._extract_one_floor(l_yamlfloors)
        # print(PrettyFormatAny.form(l_yamlfloors, 'C1-03-A'))
        # print(PrettyFormatAny.form(l_obj, 'C1-03-B'))
        self.assertEqual(l_obj.Name, '1st')
        self.assertEqual(l_obj.Comment, 'The first floor')
        self.assertEqual(l_obj.Floor, 1)

    def test_04_AllFloors(self):
        """ build the entire rooms structures
        """
        _l_node = config_tools.Yaml(self.m_pyhouse_obj).read_config_file(self.m_filename)
        _l_loc = self.m_yaml._extract_all_floors(self.m_pyhouse_obj, _l_node.Yaml)
        # print(PrettyFormatAny.form(_l_loc, 'C1-04-A - Loc'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Floors, 'C1-04-B - Floors'))
        self.assertEqual(len(self.m_pyhouse_obj.House.Floors), 4)

    def test_05_LoadConfig(self):
        """ Test that pyhouse_obj has been loaded by the 'load_yaml_config' method.
        """
        _l_floors = self.m_yaml.load_yaml_config(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'C1-05-A - House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Floors, 'C1-05-B - House.Floors'))
        # print(PrettyFormatAny.form(_l_floors, 'C1-05-C - Load'))
        self.assertEqual(self.m_pyhouse_obj.House.Floors[0].Comment, 'Anything outside the house')


class C2_YamlWrite(SetupMixin, unittest.TestCase):
    """ Write the YAML config files.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_floors = self.m_yaml.load_yaml_config(self.m_pyhouse_obj)
        self.m_working_floors = self.m_pyhouse_obj.House.Floors

    def test_01_Basic(self):
        """ Basic _test to read in data and update it so we can check for new data in output.
        """
        self.m_working_floors[0].Comment = 'After mods'
        # print(PrettyFormatAny.form(self.m_working_floors[0], 'C2-01-B'))
        # print(PrettyFormatAny.form(self.m_floors[0], 'C2-01-C'))
        self.assertEqual(self.m_working_floors[0].Comment, 'After mods')

    def test_02_Prep(self):
        """
        """
        self.m_working_floors[0].Comment = 'After mods'
        _l_ret = self.m_yaml._copy_floors_to_yaml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_working_floors[0], 'C2-02-A - Working Obj'))
        # print(PrettyFormatAny.form(l_ret, 'C2-02-B - yaml staging'))

    def test_03_Write(self):
        """
        """
        self.m_working_floors[0].Comment = 'After mods'
        _l_ret = self.m_yaml._copy_floors_to_yaml(self.m_pyhouse_obj)
        self.m_yaml.save_yaml_config(self.m_pyhouse_obj)

# ## END DBK
