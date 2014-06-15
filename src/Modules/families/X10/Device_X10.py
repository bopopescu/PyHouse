#!/usr/bin/python

"""Load the database with X10 devices.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import LightData
from Modules.lights import lighting
from Modules.utils import pyh_log


g_debug = 0

LOG = pyh_log.getLogger('PyHouse.Dev_X10     ')


class X10LightingData(LightData):

    def __init__(self):
        # lighting.LightData.__init__(self)
        self.set_family("X10")
        self.Address = 'ab'


class LightingAPI(lighting.LightingAPI):
    """Overload the base methods with specific ones here.
    """

    def extract_device_xml(self, p_device_obj, _p_entry_xml):
        """
        @param p_entry_xml: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        """
        return p_device_obj

    def insert_device_xml(self, p_entry_xml, p_device_obj):
        if p_device_obj.LightingFamily == 'Insteon':
            ET.SubElement(p_entry_xml, 'Address').text = p_device_obj.Address
            ET.SubElement(p_entry_xml, 'Controller').text = self.put_bool(p_device_obj.Controller)
            ET.SubElement(p_entry_xml, 'DevCat').text = str(p_device_obj.DevCat)
            ET.SubElement(p_entry_xml, 'GroupList').text = str(p_device_obj.GroupList)
            ET.SubElement(p_entry_xml, 'GroupNumber').text = str(p_device_obj.GroupNumber)
            ET.SubElement(p_entry_xml, 'Master').text = str(p_device_obj.Master)
            ET.SubElement(p_entry_xml, 'ProductKey').text = str(p_device_obj.ProductKey)
            ET.SubElement(p_entry_xml, 'Responder').text = self.put_bool(p_device_obj.Responder)
        elif p_device_obj.LightingFamily == 'UPB':
            try:
                ET.SubElement(p_entry_xml, 'NetworkID').text = self.put_str(p_device_obj.NetworkID)
                ET.SubElement(p_entry_xml, 'Password').text = str(p_device_obj.Password)
                ET.SubElement(p_entry_xml, 'UnitID').text = str(p_device_obj.UnitID)
            except AttributeError:
                pass

    def turn_light_off(self, p_name):
        pass

    def turn_light_on(self, p_name):
        pass

    def turn_light_dim(self, p_name, p_level):
        pass

    def scan_all_lights(self, p_lights):
        pass


class API(object):

    def __init__(self):
        """Constructor for the PLM.
        """
        pass

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Started.')

    def Stop(self, p_xml):
        return p_xml

    def ChangeLight(self, p_light_obj, p_level, p_rate = 0):
        pass

# ## END
