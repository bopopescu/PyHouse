#!/usr/bin/python

"""Load the database with UPB devices.
"""

# Import system type stuff
import logging
import xml.etree.ElementTree as ET

# Import PyMh files
from src.lights import lighting

g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 = Startup Details

g_logger = None
g_PIM = None
g_house_obj = None


class CoreData(object):

    def __init__(self):
        self.Family = 'UPB'
        self.NetworkID = None
        self.Password = None
        self.UnitID = None
        self.Command1 = 0


class CoreAPI(object):

    def load_device(self, p_dict, p_dev):
        l_dev = p_dev
        l_dev.NetworkID = self.getInt(p_dict, 'NetworkID')
        l_dev.Password = self.getInt(p_dict, 'Password')
        l_dev.UnitID = self.getInt(p_dict, 'UnitID')
        return l_dev

class ButtonData(lighting.ButtonData, CoreData):

    def __init__(self):
        super(ButtonData, self).__init__()

    def __repr__(self):
        l_str = super(ButtonData, self).__repr__()
        return l_str

class ButtonAPI(lighting.ButtonAPI, CoreAPI):
    pass


class ControllerData(lighting.ControllerData, CoreData):

    def __init__(self):
        super(ControllerData, self).__init__()

    def __repr__(self):
        l_str = super(ControllerData, self).__repr__()
        return l_str

class ControllerAPI(lighting.ControllerAPI, CoreAPI): pass


class LightData(lighting.LightData, CoreData):

    def __init__(self):
        super(LightData, self).__init__()

    def __repr__(self):
        l_str = super(LightData, self).__repr__()
        return l_str

class LightingAPI(lighting.LightingAPI, CoreAPI):
    """Interface to the lights of this module.
    """

    def extract_device_xml(self, p_entry_xml, p_device_obj):
        """
        @param p_entry_xml: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        """
        p_device_obj.NetworkID = p_entry_xml.findtext('NetworkID')
        p_device_obj.Password = p_entry_xml.findtext('Password')
        p_device_obj.UnitID = p_entry_xml.findtext('UnitID')
        return p_device_obj

    def insert_device_xml(self, p_entry_xml, p_device_obj):
        try:
            ET.SubElement(p_entry_xml, 'NetworkID').text = self.put_str(p_device_obj.NetworkID)
            ET.SubElement(p_entry_xml, 'Password').text = str(p_device_obj.Password)
            ET.SubElement(p_entry_xml, 'UnitID').text = str(p_device_obj.UnitID)
        except AttributeError:
            pass

    def load_all_lights(self, p_dict):
        if g_debug > 1:
            print "Device_UPB.load_all_lights()", p_dict
        for l_dict in p_dict.itervalues():
            l_light = LightData()
            l_light = self.load_upb_light(l_dict, l_light)
            g_house_obj.Lights[l_light.Key] = l_light

    def load_upb_light(self, p_dict, p_light):
        if g_debug > 1:
            print "Device_UPB.load_upb_light()"
        l_light = p_light
        l_light = super(LightingAPI, self).load_light(p_dict, l_light)
        l_light = self.load_device(p_dict, l_light)
        return l_light

    def change_light_setting(self, p_light_obj, p_level):
        if g_debug > 1:
            print "Device_UPB.change_light_setting()"
        if p_light_obj.Family == 'UPB':
            g_PIM.change_light_setting(p_light_obj, p_level)

    def update_all_lights(self):
        if g_debug > 1:
            print "Device_UPB.update_all_lights()"


class LoadSaveInsteonData(LightingAPI, ControllerAPI, ButtonAPI): pass


import UPB_Pim


class API(LightingAPI):

    def __init__(self, p_house_obj):
        """Constructor for the UPB .
        """
        global g_logger, g_PIM
        g_logger = logging.getLogger('PyHouse.Dev_UPB ')
        self.m_house_obj = p_house_obj
        if g_debug > 0:
            print "Device_UPB.__init__()"
        g_logger.info('Initializing.')
        g_PIM = self.m_pim = UPB_Pim.API()
        g_logger.info('Initialized.')

    def Start(self, p_house_obj):
        if g_debug > 0:
            print "Device_UPB.Start()"
        global g_house_obj
        g_house_obj = p_house_obj
        g_logger.info('Starting.')
        # self.m_pim.Start(p_house_obj)
        for l_controller_obj in p_house_obj.Controllers.itervalues():
            if l_controller_obj.Family != 'UPB':
                continue
            if l_controller_obj.Active != True:
                continue
            l_controller_obj.HandlerAPI = UPB_Pim.API()
            l_controller_obj.HandlerAPI.Start(p_house_obj, l_controller_obj)
        g_logger.info('Started.')

    def Stop(self, p_xml):
        if g_debug > 0:
            print "Device_UPB.Stop()"
        self.m_pim.Stop()
        return p_xml

    def SpecialTest(self):
        if g_debug > 0:
            print "Device_UPB.API.SpecialTest()"

# ## END