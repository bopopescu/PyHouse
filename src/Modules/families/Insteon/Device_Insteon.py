"""
-*- test-case-name: PyHouse.src.Modules.families.Insteon.test.test_Device_Insteon -*-

@name: PyHouse/src/Modules/families/Insteon/Device_Insteon.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2011-2014 by D. Brian Kimmel
@note: Created on Apr 3, 2011
@license: MIT License
@summary: This module is for Insteon

This is the main module for the Insteon family of devices.
it provides the single interface into the family.
Several other Insteon modules are included by this and are invisible to the other families.

This module loads the information about all the Insteon devices.

InsteonControllers
serial_port

"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import InsteonData
from Modules.families.Insteon import Insteon_utils
from Modules.utils import xml_tools
from Modules.utils import pyh_log
# from Modules.utils.tools import PrettyPrintAny

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.Dev_Insteon ')


class ReadWriteConfigXml(xml_tools.XmlConfigTools):

    def extract_device_xml(self, p_device_obj, p_entry_xml):
        """
        A method to extract Insteon specific elements and insert them into a basic device object.

        @param p_entry_xml: is the device's XML element
        @param p_device_obj : is the Basic Object that will have the extracted elements inserted into.
        @return: a dict of the extracted Insteon Specific data.
        """
        # LOG.debug('--- Extracting XML ')
        l_insteon_obj = InsteonData()
        l_insteon_obj.InsteonAddress = Insteon_utils.dotted_hex2int(p_entry_xml.findtext('Address', default = 0))
        l_insteon_obj.IsController = p_entry_xml.findtext('IsController')
        l_insteon_obj.DevCat = p_entry_xml.findtext('DevCat')
        l_insteon_obj.GroupList = p_entry_xml.findtext('GroupList')
        l_insteon_obj.GroupNumber = p_entry_xml.findtext('GroupNumber')
        l_insteon_obj.IsMaster = p_entry_xml.findtext('IsMaster')
        l_insteon_obj.ProductKey = p_entry_xml.findtext('ProductKey')
        l_insteon_obj.IsResponder = p_entry_xml.findtext('IsResponder')
        xml_tools.stuff_new_attrs(p_device_obj, l_insteon_obj)
        return l_insteon_obj

    def insert_device_xml(self, p_entry_xml, p_device_obj):
        ET.SubElement(p_entry_xml, 'Address').text = Insteon_utils.int2dotted_hex(int(p_device_obj.InsteonAddress))
        ET.SubElement(p_entry_xml, 'IsController').text = self.put_bool(p_device_obj.IsController)
        ET.SubElement(p_entry_xml, 'DevCat').text = str(p_device_obj.DevCat)
        ET.SubElement(p_entry_xml, 'GroupList').text = str(p_device_obj.GroupList)
        ET.SubElement(p_entry_xml, 'GroupNumber').text = str(p_device_obj.GroupNumber)
        ET.SubElement(p_entry_xml, 'IsMaster').text = str(p_device_obj.IsMaster)
        ET.SubElement(p_entry_xml, 'ProductKey').text = str(p_device_obj.ProductKey)
        ET.SubElement(p_entry_xml, 'IsResponder').text = self.put_bool(p_device_obj.IsResponder)


class API(ReadWriteConfigXml):
    """
    """

    def __init__(self):
        pass

    def Start(self, p_pyhouse_obj):
        """For the given house, this will start all the controllers for family = Insteon in that house.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_house_obj = p_pyhouse_obj.House.OBJs
        l_count = 0
        for l_controller_obj in p_pyhouse_obj.House.OBJs.Controllers.itervalues():
            if l_controller_obj.LightingFamily != 'Insteon':
                continue
            if l_controller_obj.Active != True:
                continue
            # Only one controller may be active at a time (for now).
            # But all controllers need to be processed so they may be written back to XML.
            if l_count > 0:
                l_controller_obj.Active = False
                LOG.warning('Controller {0:} skipped - another one is active.'.format(l_controller_obj.Name))
                continue
            else:
                from Modules.families.Insteon import Insteon_PLM
                self.m_plm = l_controller_obj._HandlerAPI = Insteon_PLM.API()
                if l_controller_obj._HandlerAPI.Start(p_pyhouse_obj, l_controller_obj):
                    l_count += 1
                else:
                    LOG.error('Controller {0:} failed to start.'.format(l_controller_obj.Name))
                    l_controller_obj.Active = False
        l_msg = 'Started {0:} Insteon Controllers, House:{1:}.'.format(l_count, p_pyhouse_obj.House.Name)
        LOG.info(l_msg)

    def Stop(self, p_xml):
        try:
            for l_controller_obj in self.m_house_obj.Controllers.itervalues():
                if l_controller_obj.LightingFamily != 'Insteon':
                    continue
                if l_controller_obj.Active != True:
                    continue
                l_controller_obj._HandlerAPI.Stop(l_controller_obj)
        except AttributeError:
            pass  # no controllers for house(House is being added)
        return p_xml

    def ChangeLight(self, p_light_obj, p_level, _p_rate = 0):
        if g_debug >= 1:
            LOG.debug('Change light Name:{0:}, LightingFamily:{1:}'.format(p_light_obj.Name, p_light_obj.LightingFamily))
        # PrettyPrintAny(p_light_obj, 'Light Object Device_Insteon')
        _l_api = self.m_pyhouse_obj.House.OBJs.FamilyData[p_light_obj.LightingFamily].ModuleAPI
        # PrettyPrintAny(l_api, 'Light Object Device_Insteon 2')
        self.m_plm.ChangeLight(p_light_obj, p_level)
        # if p_light_obj.LightingFamily == 'Insteon':
        #    try:
        #        for l_controller_obj in self.m_house_obj.Controllers.itervalues():
        #            if l_controller_obj.LightingFamily != 'Insteon':
        #                continue
        #            if l_controller_obj.Active != True:
        #                continue
        #            l_controller_obj._HandlerAPI.ChangeLight(p_light_obj, p_level)
        #    except AttributeError as e:  # no controllers for house. (House is being added).
        #        LOG.warning('Could not change light setting {0:}'.format(e))
        pass

# ## END DBK
