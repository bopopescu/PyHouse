"""
@name:      Modules/Computer/computer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@note:      Created on Jun 24, 2014
@license:   MIT License
@summary:   Handle the computer information.

This handles the Computer part of the node.  (The other part is "House").

"""

__updated__ = '2019-12-02'
__version_info__ = (19, 10, 5)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from datetime import datetime
import platform

#  Import PyHouse files
from Modules.Core.Config import config_tools, import_tools
from Modules.Core.Config.import_tools import Tools as importTools
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.Utilities import extract_tools, uuid_tools
from Modules.Computer.Nodes.nodes import MqttActions as nodesMqtt

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Computer       ')

CONFIG_NAME = 'computer'
MODULES = [  # All modules for the computer must be listed here.  They will be loaded if configured.
    'Bridges',
    'Communication',
    'Internet',
    'Nodes',
    'Pi',
    # 'Weather',
    'Web'
    ]
PARTS = [
    ]


class ComputerInformation:
    """
    ==> PyHouse.Computer.xxx - as in the def below.
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.UUID = None
        self.Primary = False
        self.Priority = 99
        self.Bridges = {}  # BridgeInformation() in Modules.Computer.Bridges.bridges.py
        self.Communication = {}  # CommunicationInformation()
        self.InternetConnection = {}  # InternetConnectionInformation()
        self.Nodes = {}  # NodeInformation()
        self.Weather = {}  # WeatherInformation()
        self.Web = {}  # WebInformation()


class ComputerApis:
    """
    ==> PyHouse.Computer.xxx as in the def below.

    """

    def __init__(self):
        pass


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_msg):
        """ Decode the computer specific portions of the message and append them to the log string.
        @param p_message: is the payload that is JSON
        """
        l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        p_msg.LogMessage += '\tComputer:\n'
        if l_topic[0] == 'browser':
            p_msg.LogMessage += '\tBrowser: Message {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Computer msg', 160))
        elif l_topic[0] == 'node' or l_topic[0] == 'nodes':
            p_msg.LogMessage += nodesMqtt(self.m_pyhouse_obj).decode(l_topic[1:], p_msg.Payload, p_msg.LogMessage)
        #  computer/ip
        elif l_topic[1] == 'ip':
            l_ip = extract_tools.get_mqtt_field(p_msg.Payload, 'ExternalIPv4Address')
            p_msg.LogMessage += '\tIPv4: {}'.format(l_ip)
        #  computer/startup
        elif l_topic[1] == 'startup':
            self._extract_node(p_msg.Payload)
            p_msg.LogMessage += '\tStartup {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Computer msg', 160))
            if self.m_myname == self.m_sender:
                p_msg.LogMessage += '\tMy own startup of PyHouse\n'
            else:
                p_msg.LogMessage += '\tAnother computer started up: {}'.format(self.m_sender)
        #  computer/shutdown
        elif l_topic[1] == 'shutdown':
            del self.m_pyhouse_obj.Computer.Nodes[self.m_name]
            p_msg.LogMessage += '\tSelf Shutdown {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Computer msg', 160))
        #  computer/***
        else:
            p_msg.LogMessage += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Computer msg', 160))


class Utility:
    """
    There are currently (2019) 8 components - be sure all are in every method.
    """

    m_config_tools = None
    m_import_tools = None
    m_modules_needed = ['Nodes']
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config_tools = config_tools.Yaml(p_pyhouse_obj)
        self.m_import_tools = import_tools.Tools(p_pyhouse_obj)

    def _initialize_one_module(self, p_module):
        """
        """
        l_module = p_module.lower()
        l_path = 'Modules.Computer.' + p_module
        LOG.debug('Importing: "{}", "{}"'.format(l_module, l_path))
        l_module = importTools(self.m_pyhouse_obj).import_module_get_api(l_module, l_path)
        return l_module

    def _find_all_configed_modules(self, p_module_list):
        """ we don't want to import all modules, just the ones we have config files for.
        @param p_modules: is a list of possible modules.
        @return: A list of possible modules that has a config file
        """
        l_modules = {}
        for l_module in p_module_list:
            # LOG.debug('Finding config for module "{}"'.format(l_module))
            l_path = self.m_config_tools.find_config_file(l_module.lower())
            if l_path != None:
                self.m_modules_needed.append(l_module)
                LOG.info(' Found  config file for "{}"'.format(l_module))
            else:
                LOG.info('Missing config file for "{}"'.format(l_module))
            l_modules[l_module] = l_path
        # LOG.debug('Set up modules {}'.format(p_module_list))
        return self.m_modules_needed

    def _import_all_found_modules(self, p_modules):
        """
        @param p_modules: is a list of all needed modules
        """
        l_modules = {}
        l_computer_path = 'Modules.Computer.'
        LOG.info('Needed Modules {}'.format(p_modules))
        for l_module in p_modules:
            l_path = l_computer_path + l_module.capitalize()
            l_api = self.m_import_tools.import_module_get_api(l_module, l_path)
            l_modules[l_module] = l_api
        LOG.info('Loaded Modules: {}'.format(self.m_modules_needed))
        return l_modules

    def _init_component_apis(self, p_pyhouse_obj):
        """
        Initialize all the computer division Apis
        """
        p_pyhouse_obj.Computer = ComputerApis()

    def load_module_config(self, p_modules):
        # LOG.debug('Loading Componente')
        for l_module in p_modules.values():
            l_module.LoadConfig()

    def _start_components(self):
        """
        """
        return
        l_obj = self.m_pyhouse_obj.Computer
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            l_a = getattr(l_obj, l_key)
            if l_key == 'ComputerApi':
                continue
            l_a.Start()

    def _stop_component_apis(self):
        """
        """

    def _save_component_apis(self):
        """
        """


class LocalConfig:
    """
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)
        # LOG.debug('Config - Progress')

    def _extract_computer_info(self, _p_config):
        """ The cpmputer.yamll file only contains module names to force load.

        @param p_pyhouse_obj: is the entire house object
        @param p_config: is the modules to force load.
        """
        l_modules = []
        # for l_ix, l_config in enumerate(p_config):
        #    pass
        return l_modules  # For testing.

    def load_yaml_config(self):
        """ Read the config file.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        # self.m_pyhouse_obj.Computer = None
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Computer']
        except:
            LOG.warning('The config file does not start with "Computer:"')
            return None
        l_computer = self._extract_computer_info(l_yaml)
        # self.m_pyhouse_obj.Computer = l_computer
        # LOG.debug('Computer.Yaml - {}'.format(l_yaml.Yaml))
        return l_computer  # for testing purposes


class Api:
    """
    """

    m_local_config = None
    m_modules = {}
    m_module_list = None
    m_pyhouse_obj = None
    m_utility = None

    def __init__(self, p_pyhouse_obj):
        """ Initialize the computer section of PyHouse.
        """
        LOG.info("Initializing - Version:{}".format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        self.m_utility = Utility(p_pyhouse_obj)
        #
        p_pyhouse_obj.Computer = ComputerInformation()
        p_pyhouse_obj.Computer.Name = platform.node()
        p_pyhouse_obj.Computer.Key = 0
        p_pyhouse_obj.Computer.UUID = uuid_tools.get_uuid_file(p_pyhouse_obj, CONFIG_NAME)
        p_pyhouse_obj.Computer.Comment = ''
        p_pyhouse_obj.Computer.LastUpdate = datetime.now()
        #
        l_needed_list = self.m_utility._find_all_configed_modules(MODULES)
        self.m_modules = self.m_utility._import_all_found_modules(l_needed_list)
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_local_config.load_yaml_config()
        self.m_utility.load_module_config(self.m_modules)
        LOG.info('Loaded all computer Configs.')

    def Start(self):
        """
        Start processing
        """
        LOG.info('Starting')
        self.m_utility._start_components()
        LOG.info('Started.')

    def SaveConfig(self):
        """
        Take a snapshot of the current Configuration/Status and write out an XML file.
        """
        self.m_utility._save_component_apis()
        LOG.info("Saved Computer Config.")
        return

    def Stop(self):
        """
        Append the house XML to the passed in xlm tree.
        """
        self.m_utility._stop_component_apis()
        LOG.info("Stopped.")

# ## END DBK
