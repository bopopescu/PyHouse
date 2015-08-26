"""
-*- test-case-name: PyHouse.Modules.Lighting.test.test_lighting -*-

@name:      PyHouse/src/Modules/Lighting/lighting.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2015 by D. Brian Kimmel
@note:      Created on Apr 2, 2010
@license:   MIT License
@summary:   Handle the home lighting system automation.

This is called from 'house'.
for every house.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyHouse files
from Modules.Lighting.lighting_buttons import API as buttonsAPI
from Modules.Lighting.lighting_controllers import API as controllersAPI
from Modules.Lighting.lighting_lights import API as lightsAPI
from Modules.Families.family_utils import FamUtil
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Lighting       ')


class Utility(object):
    """Commands we can run from high places.
    """

    def _setup_lighting(self, p_pyhouse_obj):
        """
        Find the lighting information
        Config file version 1.4 moved the lighting information into a separate LightingSection
        """
        l_root = p_pyhouse_obj.Xml.XmlRoot
        try:
            l_house_xml = l_root.find('HouseDivision')
        except AttributeError as e_err:
            LOG.error('House Division is missing in Config file.  {}'.format(e_err))
            l_house_xml = l_root
        try:
            l_lighting_xml = l_house_xml.find('LightingSection')
        except AttributeError as e_err:
            LOG.warning('Old version of Config file found.  No LightingSection {}'.format(e_err))
        # We have an old version
        if l_lighting_xml == None or l_lighting_xml == 'None':
            l_lighting_xml = l_house_xml
        return l_lighting_xml

    def _read_buttons(self, p_pyhouse_obj, p_xml, p_version):
        try:
            l_xml = p_xml.find('ButtonSection')
            l_ret = buttonsAPI.read_all_buttons_xml(p_pyhouse_obj, l_xml, p_version)
        except AttributeError as e_err:
            l_ret = {}
            l_msg = 'No Buttons found {}'.format(e_err)
            LOG.warning(l_msg)
            print(l_msg)
        return l_ret

    def _read_controllers(self, p_pyhouse_obj, p_xml, p_version):
        try:
            l_xml = p_xml.find('ControllerSection')
            l_ret = controllersAPI.read_all_controllers_xml(p_pyhouse_obj, l_xml, p_version)
        except AttributeError as e_err:
            l_ret = {}
            l_msg = 'No Controllers found {}'.format(e_err)
            LOG.warning(l_msg)
            print(l_msg)
        return l_ret

    def _read_lights(self, p_pyhouse_obj, p_xml, p_version):
        try:
            l_xml = p_xml.find('LightSection')
            l_ret = lightsAPI.read_all_lights_xml(p_pyhouse_obj, l_xml, p_version)
        except AttributeError as e_err:
            l_ret = {}
            l_msg = 'No Lights found: {}'.format(e_err)
            LOG.warning(l_msg)
            print(l_msg)
        return l_ret

    def _read_lighting_xml(self, p_pyhouse_obj):
        """
        Get all the lighting components for a house
        Config file version 1.4 moved the lighting information into a separate LightingSection
        """
        l_xml_version = p_pyhouse_obj.Xml.XmlOldVersion
        # l_xml_version = '1.4.0'
        l_lighting_xml = self._setup_lighting(p_pyhouse_obj)
        l_house_obj = p_pyhouse_obj.House
        l_house_obj.Controllers = self._read_controllers(p_pyhouse_obj, l_lighting_xml, l_xml_version)
        l_house_obj.Buttons = self._read_buttons(p_pyhouse_obj, l_lighting_xml, l_xml_version)
        l_house_obj.Lights = self._read_lights(p_pyhouse_obj, l_lighting_xml, l_xml_version)
        return l_house_obj

    @staticmethod
    def _write_lighting_xml(p_pyhouse_obj, p_house_element):
        l_lighting_xml = ET.Element('LightingSection')
        try:
            l_xml = lightsAPI.write_all_lights_xml(p_pyhouse_obj)
            l_lighting_xml.append(l_xml)
            l_lighting_xml.append(buttonsAPI.write_buttons_xml(p_pyhouse_obj))
            l_lighting_xml.append(controllersAPI.write_all_controllers_xml(p_pyhouse_obj))
        except AttributeError as e_err:
            l_msg = 'ERROR-109: {}'.format(e_err)
            LOG.error(l_msg)
            p_house_element.append(l_lighting_xml)
        return l_lighting_xml

    @staticmethod
    def _find_full_obj(p_pyhouse_obj, p_web_obj):
        """
        given the limited information from the web browser, look up and return the full object.

        If more than one light has the same name, return the first one found.
        """
        for l_light in p_pyhouse_obj.House.Lights.itervalues():
            if p_web_obj.Name == l_light.Name:
                return l_light
        LOG.error('ERROR - no light with name {} was found.'.format(p_web_obj.Name))
        return None


class API(Utility):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized')

    def Start(self):
        """Allow loading of sub modules and drivers.
        """
        self._read_lighting_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.APIs.House.FamilyAPI.start_lighting_families(self.m_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        """Allow cleanup of all drivers.
        """
        LOG.info("Stopping all lighting families.")
        # self.m_pyhouse_obj.APIs.House.FamilyAPI.stop_lighting_families(self.m_pyhouse_obj)
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        """ Save the Lighting section.
        It will contain several sub-sections
        """
        l_xml = Utility._write_lighting_xml(self.m_pyhouse_obj, p_xml)
        p_xml.append(l_xml)
        LOG.info("Saved Lighting XML.")
        return p_xml

    def ChangeLight(self, p_light_obj, p_source, p_new_level, _p_rate = None):
        """
        Set an Insteon controlled light to a value - On, Off, or Dimmed.

        Called by:
            web_controlLights
            schedule
        """
        l_light_obj = Utility._find_full_obj(self.m_pyhouse_obj, p_light_obj)
        try:
            LOG.info("Turn Light {} to level {}, DeviceFamily:{}".format(l_light_obj.Name, p_new_level, l_light_obj.DeviceFamily))

            l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, l_light_obj)
            l_api.ChangeLight(l_light_obj, p_source, p_new_level)
        except Exception as e_err:
            LOG.error('ERROR - {}'.format(e_err))

# ## END DBK
