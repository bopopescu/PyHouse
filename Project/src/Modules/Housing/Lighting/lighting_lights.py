"""
@name:      Modules/Housing/Lighting/lighting_lights.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2019 by D. Brian Kimmel
@note:      Created on May 1, 2011
@license:   MIT License
@summary:   This module handles the lights component of the lighting system.

Light switches such as Insteon.

Each entry should contain enough information to allow functionality of various family of lighting controllers.

Insteon is the first type coded and UPB is to follow.

The real work of controlling the devices is delegated to the modules for that family of devices.

"""

__updated__ = '2019-07-24'
__version_info__ = (19, 7, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyHouse files
from Modules.Core.data_objects import CoreLightingData
from Modules.Families.family import Config as familyConfig
from Modules.Families.family_utils import FamUtil
from Modules.Core.Utilities import extract_tools, config_tools
from Modules.Housing.Lighting.lighting_utility import Utility as lightingUtility
from Modules.Housing.rooms import Config as roomConfig
from Modules.Core.state import State
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logging
LOG = Logging.getLogger('PyHouse.LightingLights ')

CONFIG_FILE_NAME = 'lights.yaml'


class LightInformation:
    """ This is the information that the user needs to enter to uniquely define a light.
    """

    def __init__(self):
        self.Name = None
        self.Comment = None  # Optional
        self.DeviceType = 'Lighting'
        self.DeviceSubType = 'Light'
        self.LastUpdate = None  # Not user entered but maintained
        self.Uuid = None  # Not user entered but maintained
        self.Family = None  # LightFamilyInformation()
        self.Room = None  # LightRoomInformation() Optional


class LightFamilyInformation:
    """ This is the family information we need for a light

    Families may stuff other necessary information in here.
    """

    def __init__(self):
        self.Name = None
        self.Comment = None  # Optional
        self.Address = None


class LightRoomInformation:
    """ This is the room information we need for a light.
    This allows duplicate light names such as 'Ceiling' in different rooms.
    It also allows for group control by room.

    """

    def __init__(self):
        self.Name = None
        self.Comment = None  # Optional
        self.Uuid = None  # Not user entered but maintained


class LightData(CoreLightingData):
    """ This is the idealized light info.
    This class contains all the reportable and controllable information a light might have.

    ==> PyHouse.House.Lighting.Lights.xxx as in the def below
    """

    def __init__(self):
        super(LightData, self).__init__()
        self.BrightnessPct = 0  # 0% to 100%
        self.Hue = 0  # 0 to 65535
        self.Saturation = 0  # 0 to 255
        self.ColorTemperature = 0  # degrees Kelvin - 0 is not supported
        self.RGB = 0xffffff
        self.TransitionTime = 0  # 0 to 65535 ms = time to turn on or off (fade Time or Rate)
        self.State = State.UNKNOWN
        self.IsDimmable = False
        self.IsColorChanging = False
        self.Trigger = False


class MqttActions:
    """ Mqtt section
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _decode_control(self, p_message):
        """
        pyhouse/<housename>/house/lighting/light/xxx
        """
        l_control = LightData()
        l_light_name = extract_tools.get_mqtt_field(p_message, 'LightName')
        l_control.BrightnessPct = _l_brightness = extract_tools.get_mqtt_field(p_message, 'Brightness')
        # LOG.debug(PrettyFormatAny.form(l_control, 'Control', 190))
        #
        l_light_obj = lightingUtility().get_object_by_id(self.m_pyhouse_obj.House.Lighting.Lights, name=l_light_name)
        if l_light_obj == None:
            LOG.warn(' Light "{}" was not found.'.format(l_light_name))
            return
        # LOG.debug(PrettyFormatAny.form(l_light_obj, 'Light', 190))
        #
        l_controller_obj = lightingUtility().get_controller_objs_by_family(self.m_pyhouse_obj.House.Lighting.Controllers, 'Insteon')
        # LOG.debug(PrettyFormatAny.form(l_controller_obj, 'Controller', 190))
        #
        if len(l_controller_obj) > 0:
            l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, l_light_obj)
            l_api.AbstractControlLight(self.m_pyhouse_obj, l_light_obj, l_controller_obj[0], l_control)

    def decode(self, p_topic, p_message):
        """ Decode Mqtt message
        ==> pyhouse/<house name>/house/lighting/light/<action>

        @param p_topic: is the topic after 'lighting'
        @return: a message to be logged as a Mqtt message
        """
        l_logmsg = '\tLighting/Lights: {}\n\t'.format(p_topic)
        # LOG.debug('LightingLightsDispatch Topic:{}\n\t{}'.format(p_topic, p_message))
        if p_topic[0] == 'control':
            self._decode_control(p_message)
            l_logmsg += 'Light Control: {}'.format(PrettyFormatAny.form(p_message, 'Light Control'))
            LOG.debug('MqttLightingLightsDispatch Control Topic:{}\n\t{}'.format(p_topic, p_message))
        elif p_topic[0] == 'status':
            # The status is contained in LightData() above.
            # l_logmsg += 'Light Status: {}'.format(PrettyFormatAny.form(p_message, 'Light Status'))
            l_logmsg += 'Light Status: {}'.format(p_message)
            LOG.debug('MqttLightingLightsDispatch Status Topic:{}\n\t{}'.format(p_topic, p_message))
        else:
            l_logmsg += '\tUnknown Lighting/Light sub-topic:{}\n\t{}'.format(p_topic, PrettyFormatAny.form(p_message, 'Light Status'))
            LOG.warn('Unknown Lights Topic: {}'.format(p_topic[0]))
        return l_logmsg


class Config:
    """ The major work here is to load and save the information about a light switch.
    """

    def _extract_room(self, p_config):
        """ Get the room and position within the room of the device.
        """
        l_ret = roomConfig().load_room_config(p_config)
        return l_ret

    def _extract_family(self, p_config):
        """
        """
        l_ret = familyConfig().load_family_config(p_config, self.m_pyhouse_obj)
        return l_ret

    def _extract_one_light(self, p_config) -> dict:
        """ Extract the config info for one Light.
        - Name: Light 1
          Comment: This is test light 1
          Family:
             Name: Insteon
             Address: 11.44.33
          Dimmable: true  # Optional
          Room:
             Name: Living Room
        @param p_config: is the config fragment containing one light's information.
        @return: a LightInformation() obj filled in.
        """
        l_obj = LightInformation()
        l_required = ['Name', 'Family']
        for l_key, l_value in p_config.items():
            # print('Light Key: {}; Val: {}'.format(l_key, l_val))
            if l_key == 'Family':
                l_ret = self._extract_family(l_value)
                l_obj.Family = l_ret
            elif l_key == 'Room':
                l_ret = self._extract_room(l_value)
                l_obj.Room = l_ret
                pass
            else:
                setattr(l_obj, l_key, l_value)
        # Check for required data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('Location Yaml is missing an entry for "{}"'.format(l_key))
        return l_obj

    def _extract_all_lights(self, p_config):
        """ Get all of the lights configured
        """
        l_dict = {}
        for l_ix, l_light in enumerate(p_config):
            # print('Light: {}'.format(l_light))
            l_light_obj = self._extract_one_light(l_light)
            l_dict[l_ix] = l_light_obj
        return l_dict

    def LoadYamlConfig(self, p_pyhouse_obj):
        """ Read the lights.yaml file if it exists.  No file = no lights.
        It must contain 'Lights:'
        All the lights are a list.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Loading _Config - Version:{}'.format(__version__))
        try:
            l_node = config_tools.Yaml(p_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        except:
            p_pyhouse_obj.House.Lighting.Lights = None
            return None
        try:
            l_yaml = l_node.Yaml['Lights']
        except:
            LOG.warn('The lights.yaml file does not start with "Lights:"')
            p_pyhouse_obj.House.Lighting.Lights = None
            return None
        l_lights = self._extract_all_lights(l_yaml)
        p_pyhouse_obj.House.Lighting.Lights = l_lights
        return l_lights  # for testing purposes

# -------------

    def _copy_to_yaml(self, p_pyhouse_obj):
        """ Create or Update the yaml information.
        The information in the YamlTree is updated to be the same as the running pyhouse_obj info.

        The running info is a dict and the yaml is a list!

        @return: the updated yaml ready information.
        """
        try:
            l_node = p_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME]
            l_config = l_node.Yaml['Lights']
        except Exception as e_err:
            LOG.info('No Lights yaml file - creating a new file - {}'.format(e_err))
            l_node = config_tools.Yaml(p_pyhouse_obj).create_yaml_node('Lights')
            l_config = l_node.Yaml['Lights']
        l_working = p_pyhouse_obj.House.Lighting.Lights
        LOG.debug(PrettyFormatAny.form(l_working, 'Working lights', 190))
        for l_key in [l_attr for l_attr in dir(l_working) if not l_attr.startswith('_')  and not callable(getattr(l_working, l_attr))]:
            l_val = getattr(l_working, l_key)
            setattr(l_config, l_key, l_val)
            LOG.debug('Key:{}'.format(l_key))
        # p_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME].Yaml['Lights'] = l_config
        l_ret = {'Lights': l_config}
        return l_ret

    def _build_yaml(self):
        """
        """

    def _save_one_light(self, p_light_obj):
        """ Create a Yaml map of all light attributes to save
        """
        LOG.debug('Saving one light: {}'.format(p_light_obj))
        l_ret = p_light_obj.Name
        return l_ret

    def _save_all_lights(self, p_pyhouse_obj, p_config):
        """ Lights are list items

        @param p_config: is the yaml['Lights'] structure
        @return: a complete yaml tree ready to save
        """
        LOG.debug(p_config)
        l_lights = p_pyhouse_obj.House.Lighting.Lights
        for l_light_obj in l_lights.values():
            l_config = self._save_one_light(l_light_obj)
            try:
                LOG.debug('Inserting one light')
                p_config.insert(-1, l_config)
            except:
                LOG.debug('Create a list of lights')
            # p_config[-1] = l_config
        return p_config

    def SaveYamlConfig(self, p_pyhouse_obj):
        """ Save all the lights in a separate yaml file.
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        try:
            l_node = p_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME]
            l_config = l_node.Yaml['Lights']
        except Exception as e_err:
            LOG.info('No Lights yaml file - creating a new file - {}'.format(e_err))
            l_node = config_tools.Yaml(p_pyhouse_obj).create_yaml_node('Lights')
            p_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME] = l_node
            l_config = l_node.Yaml['Lights']
        l_config = self._save_all_lights(p_pyhouse_obj, l_config)
        config_tools.Yaml(p_pyhouse_obj).write_yaml(l_config, CONFIG_FILE_NAME, addnew=True)
        return l_config


class API(MqttActions):
    """
    """

    def __init__(self, p_pyhouse_obj):
        # p_pyhouse_obj.House.Lighting.Lights = {}
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """
        """
        LOG.info('Load Config')
        Config().LoadYamlConfig(self.m_pyhouse_obj)
        LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting, 'Lighting_lights.API.LoadConfig', 190))
        return {}

    def SaveConfig(self):
        """ Save the Lighting section.
        It will contain several sub-sections
        """
        LOG.info('Save Config')
        Config().SaveYamlConfig(self.m_pyhouse_obj)

    def AbstractControlLight(self, p_device_obj, p_controller_obj, p_control):
        """
        Insteon specific version of control light
        All that Insteon can control is Brightness and Fade Rate.

        @param p_controller_obj: optional
        @param p_device_obj: the device being controlled
        @param p_control: the idealized light control params
        """
        if self.m_plm == None:
            LOG.info('No PLM was defined - Quitting.')
            return
        l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, p_device_obj)
        l_api.AbstractControlLight(p_device_obj, p_controller_obj, p_control)

#  ## END DBK
