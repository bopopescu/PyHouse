#!/usr/bin/env python

"""Handle the home lighting system automation.

There are a number of lighting 'Family' types handled here.
The Insteon family is now functional.
The UPB family is work in progress
The X-10 family is mostly just a stub at present (2012)
New lighting families are added to this module.

Each family consists of four major areas:
    Lights / Lighting Devices
    Controllers - connected to the computer
    Scenes - have one or more lights that are controlled together
    Buttons - extra buttons with no light directly attached (key-pad-link)

This is a Main Module - always present.

    *!* - These are the places to add new lighting family information
"""

# Import system type stuff
import logging
import importlib

# Import PyMh files
import configure
import lighting_buttons
import lighting_controllers
import lighting_lights
import lighting_scenes
import lighting_status

#from tools import Lister


# These globals in the lighting singleton hold the operating data loaded at startup.
Button_Data = lighting_buttons.Button_Data
Controller_Data = lighting_controllers.Controller_Data
Light_Data = lighting_lights.Light_Data
Light_Status = lighting_status.Light_Status
Scene_Data = lighting_scenes.Scene_Data
Singletons = {}

g_debug = 0
g_reactor = None
g_logger = None
g_family_module = []
g_Device_family = []

' *!* Modules and pointers to the modules'
from families import VALID_FAMILIES
VALID_INTERFACES = ['Serial', 'USB', 'Ethernet']

m_InsteonDevice = None
m_X10Device = None
m_UpbDevice = None


class ButtonData(lighting_buttons.ButtonsData): pass

class ButtonAPI(lighting_buttons.ButtonsAPI): pass


class ControllerData(lighting_controllers.ControllersData): pass

class ControllerAPI(lighting_controllers.ControllersAPI): pass


class LightingData(lighting_lights.LightsData): pass

class LightingAPI(lighting_lights.LightsAPI): pass


class LightingStatusData(lighting_status.LightingStatusData): pass

class LightingStatusAPI(lighting_status.LightingStatusAPI): pass


class SceneData(lighting_scenes.ScenesData): pass

class SceneAPI(lighting_scenes.ScenesAPI): pass


class LightingUtility(ButtonAPI, ControllerAPI, LightingAPI, LightingStatusAPI):
    """
    """

    def _load_all_lighting_families(self):
        """
        Get all the config information for all types of lights and scenes.
        """
        g_logger.info("Loading all lighting families.")
        for l_family in VALID_FAMILIES:
            #l_name = 'Device_' + l_family
            l_package = 'families.' + l_family
            l_import = '.Device_' + l_family
            if g_debug: print "lighting.load_all_lighting_families - Package:{0:}, Import:{1:}".format(l_package, l_import)
            l_module = importlib.import_module(l_package + l_import, l_package)
            g_family_module.append(l_module)
            g_Device_family.append(l_import)
            l_module.Init()

    def load_lighting_xml(self):
        configure.config_xml.ReadConfig().read_lights()
        self._load_all_lighting_families()

    def _dump_all_lighting_families(self):
        self.dump_all_buttons()
        self.dump_all_controllers()
        self.dump_all_lights()

    def _start_all_lighting_families(self, p_reactor):
        if g_debug: print "lighting start all lighting"
        g_logger.info("Starting all lighting families.")
        for l_module in g_family_module:
            l_module.Start(p_reactor)

    def _stop_all_lighting_families(self):
        g_logger.info("Stopping all lighting families.")
        for l_module in g_family_module:
            l_module.Stop()

    def change_light_setting(self, p_name, p_level = 0, _p_family = None):
        """ *!* API
        Turn a light to a given level (0-100) off/dimmed/on.
        The schedule does not know what the family that controls the light.
        """
        g_logger.info("Turn Light {0:} to level {1:}.".format(p_name, p_level))
        for l_module in g_family_module:
            if g_debug: print " Processing Module ", l_module
            l_module.LightingAPI().change_light_setting(p_name, p_level)

    def update_all_lighting_families(self):
        """ *!*  API
        Update the light configs in the appropriate module.
        """
        g_logger.info("Updating all lighting families.")
        for l_module in g_family_module:
            l_module.LightingAPI().update_all_lights()

    def scan_all_lighting(self, p_lights):
        """ *!*
        """
        return
        if self.m_InsteonDevice != None:
            self.m_InsteonDevice.scan_all_lights(p_lights)
        if self.m_UpbDevice != None:
            self.m_UpbDevice.scan_all_lights(p_lights)
        if self.m_X10Device != None:
            self.m_X10Device.scan_all_lights(p_lights)


def Init():
    global g_logger
    g_logger = logging.getLogger('PyHouse.Lighting')
    g_logger.info("Initializing")
    LightingUtility().load_lighting_xml()
    #SceneAPI().load_all_scenes(configure_mh.Configure_Data['Scenes'])
    g_logger.info("Initialized.")

def Start(p_reactor):
    """Allow loading of sub modules and drivers.
    """
    LightingUtility()._start_all_lighting_families(p_reactor)

def Stop():
    """Allow cleanup of all drivers.
    """
    LightingUtility()._stop_all_lighting_families()

### END
