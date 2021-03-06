"""
@name:      Modules/House/Security/garage_door.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on aug 26, 2019
@Summary:

"""

__updated__ = '2019-12-29'
__version_info__ = (19, 10, 2)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff

# Import PyMh files
from Modules.Core.Config.config_tools import Api as configApi

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.GarageDoor     ')

CONFIG_NAME = 'garagedoors'


class GarageDoorInformation:
    """

    ==> PyHouse.House.Security.Garage_Doors.xxx as in the def below
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.DeviceType = 'Security'
        self.DeviceSubType = 'GarageDoor'
        self.Family = None  # FamilyInformation()
        self.Room = None  # RoomInformation()
        self.Status = None  # Open | Closed


class LocalConfig:
    """
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_one_garage_door(self, p_config) -> dict:
        """ Extract the config info for one button.
        - Name: Button 1
          Comment: This is _test button 1
          Family:
             Name: Insteon
             Address: 11.44.33
          Dimmable: true  # Optional
          Room:
             Name: Living Room
        @param p_config: is the config fragment containing one button's information.
        @return: a ButtonInformation() obj filled in.
        """
        l_obj = GarageDoorInformation()
        l_required = ['Name', 'Family']
        for l_key, l_value in p_config.items():
            if l_key == 'Family':
                l_obj.Family = self.m_config.extract_family_group(l_value)
            elif l_key == 'Room':
                l_obj.Room = self.m_config.extract_room_group(l_value)
                pass
            else:
                setattr(l_obj, l_key, l_value)
        # Check for required data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('Location Yaml is missing an entry for "{}"'.format(l_key))
        LOG.info('Extracted Garage Door "{}"'.format(l_obj.Name))
        return l_obj

    def _extract_all_garage_doors(self, p_config):
        """ Get all of the button sets configured
        A Button set is a (mini-remote) with 4 or 8 buttons in the set
        The set has one insteon address and each button is in a group
        """
        l_dict = {}
        for l_ix, l_button in enumerate(p_config):
            # print('Light: {}'.format(l_light))
            l_gdo_obj = self._extract_one_garage_door(l_button)
            l_dict[l_ix] = l_gdo_obj
        return l_dict

    def load_yaml_config(self):
        """ Read the lights.yaml file if it exists.  No file = no lights.
        It must contain 'Lights:'
        All the lights are a list.
        """
        l_yaml = self.m_config.read_config_file(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Garage_Doors']
        except:
            LOG.warning('The config file does not start with "Garage_Doors:"')
            return None
        l_gdo = self._extract_all_garage_doors(l_yaml)
        return l_gdo


class Api:
    """
    """
    m_pyhouse_obj = None
    m_local_config = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def _add_storage(self) -> None:
        """
        """
        self.m_pyhouse_obj.House.Security.Garage_Doors = {}

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config')
        self.m_pyhouse_obj.House.Security.Garage_Doors = self.m_local_config.load_yaml_config()
        LOG.info('Loaded {} Garage Door(s).'.format(len(self.m_pyhouse_obj.House.Security.Garage_Doors)))

    def Start(self):
        """
        """

    def SaveConfig(self):
        """
        """
        pass

    def Stop(self):
        """
        """
        pass

# ## END DBK
