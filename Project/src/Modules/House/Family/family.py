"""
@name:      Modules/House/Family/family.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@note:      Created on May 17, 2013
@license:   MIT License
@summary:   This module is for *BUILDING/loading* device families.

Families are a way of abstracting the difference between different "Device Families".
Device families are things such as Insteon, X10, Zigby and many others.
Each family has a different syntax for communicating with the various devices in that family.

Insteon, for example, has light switches, dimmers, light bulbs, thermostats, cameras to name a few.

So far Insteon and UPB are developed.  Many others may be added.

The goal of this module is to fill in enough info in each family object to allow information that is specific
 to a family to be loaded/saved between a device object and the config file.

The Family specific information is used to control and monitor the different devices within the family.

An Insteon_device module is used to read and write information to an Insteon controller connected to the computer.

    FamilyPackageName         Will point to the package directory 'Modules.House.Family.insteon'
    FamilyDevice_ModuleName   will contain 'Insteon_device'
    FamilyXml_ModuleName      will contain 'Insteon_xml'

    DeviceAPI    will point to Insteon_device.API() to allow API functions to happen.
    FamilyXml_ModuleAPI       will point to Insteon_xml.API() where ReadXml
    FamilyYaml_ModuleAPI      will point to Insteon_yaml.API() where LoadConfig

"""

__updated__ = '2019-08-15'

# Import system type stuff
import importlib

# Import PyHouse files
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Family         ')

CONFIG_FILE_NAME = 'families.yaml'


class FamilyModuleInformation:
    """ A container for every family that has been defined in modules.

    PyHouse_obj.House.Family.()
    PyHouse_obj.House.Family is a dict indexed by lower() family name.

    Each entry is an object of this class.
    """

    def __init__(self):
        self.Name = None
        self.DeviceName = None  # insteon_device
        # self.ConfigName = None  # insteon_yaml
        self.PackageName = None  # Modules.House.Family.insteon
        self.DeviceAPI = None  # insteon_device.API()
        # self.ConfigAPI = None


class FamilyConfigInformation:
    """
    """

    def __init__(self):
        self.Name = None


class Utility:
    """
    This will go thru every valid family and build a family entry for each one.
    It also imports the _device and _xml for each family and stores their API reference in the family object.

    This should operate more as a plug-in loader rather than loading everything.
    """

    def _do_import(self, p_family_obj, p_module_name):
        """
        Import a module given its name. 'Insteon_device' or 'Hue_config'

        @param p_family_obj: is a family Object.
        @param p_module_name: is a name of a module that we want to import ('Insteon_device')
        @return: the imported module object or None
        """
        l_package = p_family_obj.PackageName  # contains e.g. 'Modules.House.Family.insteon'
        l_module = l_package + '.' + p_module_name
        try:
            l_ret = importlib.import_module(l_module, package=l_package)
        except ImportError as e_err:
            l_msg = 'ERROR importing family:{};  Module:{}\n\tErr:{}.'.format(p_family_obj.Name, p_module_name, e_err)
            LOG.error(l_msg)
            l_ret = None
        return l_ret

    def _create_api_instance(self, p_pyhouse_obj, p_module_name, p_module_ref):
        """
        Hopefully, this will catch errors when adding new families.
        I had a very strange error when one module had a different number of params in the API.__init__ definition.

        @param p_pyhouse_obj: is the entire PyHouse Data
        @param p_module_name: is the name of the module for which we are creating the API instance.
        @param p_module_ref: is a reference to the module we just imported.
        """
        try:
            l_api = p_module_ref.API(p_pyhouse_obj)
        except Exception as e_err:
            LOG.error('ERROR - Module: {}\n\t{}'.format(p_module_name, e_err))
            LOG.error('Ref: {}'.format(PrettyFormatAny.form(p_module_ref, 'ModuleRef', 190)))
            l_api = None
        return l_api

    def _create_config_instance(self, _p_pyhouse_obj, p_module_name, p_module_ref):
        """
        @param p_module_name: is the name of the module for which we are creating the API instance.
        @param p_module_ref: is the module we just imported.
        """
        try:
            l_api = p_module_ref.Config()
            return l_api
        except Exception as e_err:
            LOG.error('ERROR - Module:{} - {}'.format(p_module_name, e_err))
        return None

    def _build_module_names(self, p_name):
        """
        """
        l_name = p_name.lower()
        LOG.debug('Building names for "{}"'.format(l_name))
        l_obj = FamilyModuleInformation()
        l_obj.Name = l_name
        l_obj.PackageName = 'Modules.House.Family.' + l_name
        l_obj.DeviceName = l_name + '_device'
        # l_obj.ConfigName = l_name + '_config'
        return l_obj

    def _build_one_family_data(self, p_pyhouse_obj, p_name):
        """Build up the FamilyModuleInformation names portion entry for a single family

        For the Insteon family:
            insteon_device                   ==> FamilyDevice_ModuleName
            insteon_xml                      ==> FamilyXml_ModuleName
            insteon_yaml                     ==> FamilyYaml_ModuleName
            Modules.House.Family.insteon         ==> PackageName

        @param p_name: a Valid Name such as "Insteon"
        """
        # l_name = config_tools.Yaml(p_pyhouse_obj).find_first_element(p_name)
        LOG.info('Building Family: {}'.format(p_name))
        l_family_obj = self._build_module_names(p_name)
        # Now import the family python package and 2 modules
        importlib.import_module(l_family_obj.PackageName)
        l_device_ref = Utility()._do_import(l_family_obj, l_family_obj.DeviceName)
        l_family_obj.DeviceAPI = Utility()._create_api_instance(p_pyhouse_obj, l_family_obj.DeviceName, l_device_ref)
        # l_config_ref = Utility()._do_import(l_family_obj, l_family_obj.ConfigName)
        # l_family_obj.ConfigAPI = Utility()._create_config_instance(p_pyhouse_obj, l_family_obj.ConfigName, l_config_ref)
        LOG.debug(PrettyFormatAny.form(l_family_obj, 'Family'))
        return l_family_obj


class Config:
    """
    """

    def load_family_config(self, p_config, p_pyhouse_obj):
        """ Get the yaml config information.

        This is called from many different modules.
        It loads the appropriate information for the different families supported by PyHouse

        Family:
           Name: Insteon
           Address: 11.44.33

        """
        l_obj = FamilyConfigInformation()
        l_module = FamilyModuleInformation()
        l_required = ['Name']
        #
        # Load specific family information dispatched from here
        #
        for l_key, l_value in p_config.items():
            if l_key == 'Name':
                l_value = l_value.lower()
                p_pyhouse_obj.House.Family[l_value] = l_obj
            setattr(l_obj, l_key, l_value)
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('Controller Yaml is missing an entry for "{}"'.format(l_key))

        # Now build the families actually called for in the config files.
        # LOG.debug(PrettyFormatAny.form(p_pyhouse_obj.House.Family, 'House.Family', 190))
        try:
            _l_test = p_pyhouse_obj.House.Family[l_obj.Name]
        except Exception as e_err:
            LOG.debug('Config family "{}" Update family.\n\tError: {}'.format(l_obj.Name, e_err))
            LOG.debug(PrettyFormatAny.form(p_pyhouse_obj, 'PyHouse'))
            LOG.debug(PrettyFormatAny.form(p_pyhouse_obj.House, 'House'))
            LOG.debug(PrettyFormatAny.form(p_pyhouse_obj.House.Family, 'Family'))
            l_module.Name = l_obj.Name
            p_pyhouse_obj.House.Family[l_obj.Name] = l_module
        return l_obj


class API:

    m_count = 0
    m_family = {}

    def __init__(self, p_pyhouse_obj):
        p_pyhouse_obj.House.Family = self.m_family
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized')

    def LoadConfig(self):
        """
        Build p_pyhouse_obj House Family
        """
        # LOG.debug('Reloading Families')
        # self.m_pyhouse_obj.House.Family = self.m_family
        pass

    def Start(self):
        """
        """
        LOG.info("Starting all families.")
        for l_fam, l_family_obj in self.m_pyhouse_obj.House.Family.items():
            LOG.info('Starting Family {}'.format(l_family_obj.Name))
            LOG.debug(PrettyFormatAny.form(l_family_obj, 'PyHouse Family'))
            l_family_obj = Utility()._build_one_family_data(self.m_pyhouse_obj, l_family_obj.Name)
            self.m_pyhouse_obj.House.Family[l_fam] = l_family_obj
            l_family_obj.DeviceAPI.Start()
        LOG.info("Started all lighting families.")
        return self.m_family

    def SaveConfig(self):
        """
        The family section is not saved.  it is rebuilt every Start() time from the lighting info
        """
        # LOG.info("Saved Config.")

    def LoadFamilyTesting(self):
        """
        Load all the families for testing.
        """
        # return Utility()._init_family_component_apis(self.m_pyhouse_obj)
        pass

# ## END DBK
