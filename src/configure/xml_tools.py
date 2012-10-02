#!/usr/bin/env python

"""This module only used by config_xml to access or create an empty config file.1
0
"""

# A standard series of paths that leasd to the config file.

import os, sys
from xml.etree import ElementTree as ET
from xml.dom import minidom

class ConfigFile(object):
    
    m_std_path = '/etc/PyHouse/', '~/.PyHouse/', '/var/PyHouse/'
    m_std_name = 'PyHouse.xml'

    def __init__(self):
        pass

    def create_find_config_dir(self):
        """Check for directory existance.  If not, try creating one.
        If we can't create one, return a failure.

        @return: the path we created or found
        """
        #print "Create_config_dir()"
        for l_dir in self.m_std_path:
            #print "1. Processing dir ", l_dir
            l_dir = os.path.expanduser(l_dir)
            if os.path.exists(l_dir):
                #print "Found directory path ", l_dir
                return l_dir
        print "No directory found, try creating one."
        for l_dir in self.m_std_path:
            #print "2, Processing dir ", l_dir
            l_dir = os.path.expanduser(l_dir)
            try:
                os.mkdir(l_dir)
                #print "Directory created - ", l_dir
                return l_dir
            except OSError:
                #print "Could not make a directory -", l_dir
                pass
        print "Could not create any of the following ", self.m_std_path
        sys.exit(1)

    def find_config_file(self, p_dir):
        """Add a file name to the passed in dir to get the config file.
        """
        l_file_name = os.path.join(p_dir, self.m_std_name)
        try:
            open(l_file_name, mode='r')
        except IOError:
            self.create_empty_config_file(l_file_name)
        return l_file_name

    def create_empty_config_file(self, p_name):
        """Create an empty skeleton XML config file.

        @param p_name: the complete path and filename to create.
        """
        print "xml_tools create_empty_config_file"
        l_top = ET.Element('PyHouse')
        l_comment = ET.Comment('Generated by PyHouse')
        l_top.append(l_comment)
        #l_log = ET.SubElement(l_top, 'LogFiles')
        #l_house = ET.SubElement(l_top, 'Houses')
        #l_sched = ET.SubElement(l_top, 'Schedules')
        #l_light = ET.SubElement(l_top, 'Lighting')
        #l_web = ET.SubElement(l_top, 'WebServer')
        open(os.path.expanduser(p_name), 'w')
        l_nice = prettify(l_top)
        print l_nice
        ET.ElementTree(l_top).write(p_name)


def prettify(elem):
    """Return a pretty-printed XML string for the Element.

    @param elem: an element to format as a readable xml tree.
    @return: a string formatted with indeentation and newlines.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def open_config():
    """Open the PyHouse config xml file.

    If the file is not found, create a skeleton xml file to be populated by the user via the GUI.

    Search in several standard places for the config file;
    if not found create it after checking for read write permissions.

    @return: the open file name
    """
    l_cf = ConfigFile()
    l_dir = l_cf.create_find_config_dir()
    l_file = l_cf.find_config_file(l_dir)
    try:
        open(l_file, mode='r')
    except Exception, e: # IOError:
        print " -- Error in open_config ", sys.exc_info(), e           
        l_file = '~/.PyHouse/PyHouse.xml'
        l_file = os.path.expanduser(l_file)
        ConfigFile().create_empty_config_file(l_file)
    return l_file

### END