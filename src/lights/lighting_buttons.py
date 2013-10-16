#!/usr/bin/env python

"""Handle the controller component of the lighting system.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyHouse files
from src.lights import lighting_core


g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 = xml read / write


class ButtonData(lighting_core.CoreData):

    def __init__(self):
        super(ButtonData, self).__init__()
        self.Type = 'Button'

    def __str__(self):
        l_str = super(ButtonData, self).__str__()
        return l_str

    def reprJSON(self):
        l_ret = super(ButtonData, self).reprJSON()  # The core data
        return l_ret


class ButtonsAPI(lighting_core.CoreAPI):
    """
    """

    def __init__(self):
        super(ButtonsAPI, self).__init__()

    def read_button_xml(self, p_house_obj, p_house_xml):
        """
        """
        if g_debug >= 2:
            print "lighting_buttons.read_button_xml() - House:{0:}".format(p_house_obj.Name)
        l_count = 0
        l_dict = {}
        l_sect = p_house_xml.find('Buttons')
        l_list = l_sect.iterfind('Button')
        for l_entry in l_list:
            l_button_obj = ButtonData()
            l_button_obj = self.read_light_common(l_entry, l_button_obj, p_house_obj)
            l_button_obj.Key = l_count  # Renumber
            l_dict[l_count] = l_button_obj
            l_count += 1
        p_house_obj.Buttons = l_dict
        if g_debug >= 6:
            print "lighting_buttons.read_button_xml()  loaded {0:} buttons for house {1:}".format(l_count, p_house_obj.Name)
        return l_dict

    def write_button_xml(self, p_house_obj):
        if g_debug >= 2:
            print "lighting_buttons.write_button+xml()"
        l_count = 0
        l_buttons_xml = ET.Element('Buttons')
        for l_button_obj in p_house_obj.Buttons.itervalues():
            l_entry = self.xml_create_common_element('Button', l_button_obj)
            self.write_light_common(l_entry, l_button_obj, p_house_obj)
            l_buttons_xml.append(l_entry)
            l_count += 1
        if g_debug >= 6:
            print "lighting_buttons.write_button_xml() - Wrote {0:} buttons".format(l_count)
        return l_buttons_xml


# ## END DBK
