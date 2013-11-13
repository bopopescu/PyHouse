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

g_logger = logging.getLogger('PyHouse.Device_UPB  ')


class CoreData(object):

    def __init__(self):
        super(CoreData, self).__init__()
        self.Family = 'UPB'
        self.NetworkID = None
        self.Password = None
        self.UnitID = None

    def reprJSON(self):
        print "Device_UPB.reprJSON(1)"
        l_ret = super(CoreData, self).reprJSON()  # The core data
        l_ret.update(dict(
                    Address = self.UnitID, Password = self.Password, NetworkId = self.NetworkID
                    ))
        return l_ret


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

    def __str__(self):
        l_str = super(ButtonData, self).__str__()
        return l_str

class ButtonAPI(lighting.ButtonAPI, CoreAPI):
    pass


class ControllerData(lighting.ControllerData, CoreData):

    def __init__(self):
        super(ControllerData, self).__init__()

    def __str__(self):
        l_str = super(ControllerData, self).__str__()
        return l_str

class ControllerAPI(lighting.ControllerAPI, CoreAPI): pass


class LightData(lighting.LightData, CoreData):

    def __init__(self):
        super(LightData, self).__init__()

    def __str__(self):
        l_str = super(LightData, self).__str__()
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


class LoadSaveInsteonData(LightingAPI, ControllerAPI, ButtonAPI): pass

import UPB_Pim


class API(LightingAPI):

    def __init__(self, p_house_obj):
        """Constructor for the UPB.
        """
        self.m_house_obj = p_house_obj

    def Start(self, p_house_obj):
        self.m_house_obj = p_house_obj
        for l_controller_obj in self.m_house_obj.Controllers.itervalues():
            if l_controller_obj.Family != 'UPB':
                continue
            if l_controller_obj.Active != True:
                continue
            g_logger.info('Starting UPB family')
            l_controller_obj._HandlerAPI = UPB_Pim.API()
            l_controller_obj._HandlerAPI.Start(self.m_house_obj, l_controller_obj)
        g_logger.info('Started.')

    def Stop(self, p_xml):
        if g_debug > 0:
            print "Device_UPB.Stop()"
        try:
            for l_controller_obj in self.m_house_obj.Controllers.itervalues():
                if l_controller_obj.Family != 'UPB':
                    continue
                if l_controller_obj.Active != True:
                    continue
                l_controller_obj._HandlerAPI.Stop(l_controller_obj)
        except AttributeError:
            pass  # no controllers for house(House is being added)
        return p_xml

    def ChangeLight(self, p_light_obj, p_level, _p_rate = 0):
        try:
            for l_controller_obj in self.m_house_obj.Controllers.itervalues():
                if (l_controller_obj.Family == 'UPB') and (l_controller_obj.Active == True):
                    l_controller_obj._HandlerAPI.ChangeLight(p_light_obj, p_level)
        except AttributeError:
            pass  # no controllers for house(House is being added)

# ## END
