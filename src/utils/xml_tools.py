#!/usr/bin/env python

"""This module used to access or create an empty config file.1
0
"""

# Import system type stuff
import datetime
import os
import sys
import uuid
from xml.etree import ElementTree as ET
from xml.dom import minidom

# Import PyMh files


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 - Config file handling
# 4 = Debug do get_xxx_element
# + = NOT USED HERE
g_xmltree = None


class PutGetXML(object):
    """Protected put / get routines

    Try to be safe if a user edits the XML file.
    """
#-----
# Bool
#-----
    def get_bool_from_xml(self, p_xml, p_name, p_default = False):
        l_xml = p_xml.find(p_name)  # Element
        if l_xml == None:
            l_xml = p_xml.get(p_name)  # Attribute
        else:
            l_xml = l_xml.text
        l_ret = p_default
        if l_xml == 'True' or l_xml == True:
            l_ret = True
        return l_ret

    def put_bool_attribute(self, p_xml_element, p_bool = 'False'):
        l_bool = 'False'
        if p_bool == True or p_bool == 'True':
            l_bool = 'True'
        p_xml_element.put(l_bool)

    def put_bool_element(self, p_parent_xml, p_name, p_bool = 'False'):
        l_bool = 'False'
        if p_bool == True or p_bool == 'True':
            l_bool = 'True'
        ET.SubElement(p_parent_xml, p_name).text = l_bool

#-----
# float
#-----
    def get_float_from_xml(self, p_xml, p_name, p_default = 0.0):
        l_xml = p_xml.find(p_name)
        if l_xml == None:
            l_xml = p_xml.get(p_name)
        else:
            l_xml = l_xml.text
        try:
            l_var = float(l_xml)
        except (ValueError, TypeError):
            l_var = p_default
        return l_var

    def put_float_attribute(self, p_xml_element, p_name, p_float):
        try:
            l_var = str(p_float)
        except (ValueError, TypeError):
            l_var = '0.0'
        p_xml_element.set(p_name, l_var)

    def put_float_element(self, p_parent_element, p_name, p_float):
        try:
            l_var = str(p_float)
        except (ValueError, TypeError):
            l_var = '0.0'
        ET.SubElement(p_parent_element, p_name).text = l_var

#-----
# int
#-----
    def get_int_from_xml(self, p_xml, p_name, p_default = 0):
        l_xml = p_xml.find(p_name)
        if l_xml == None:
            l_xml = p_xml.get(p_name)
        else:
            l_xml = l_xml.text
        try:
            l_var = int(l_xml)
        except (ValueError, TypeError):
            l_var = p_default
        return l_var

    def put_int_attribute(self, p_xml_element, p_name, p_int):
        try:
            l_var = str(p_int)
        except (ValueError, TypeError):
            l_var = '0'
        p_xml_element.set(p_name, l_var)

    def put_int_element(self, p_parent_element, p_name, p_int):
        try:
            l_var = str(p_int)
        except (ValueError, TypeError):
            l_var = '0'
        ET.SubElement(p_parent_element, p_name).text = l_var

#-----
# text
#-----
    def get_text_from_xml(self, p_xml, p_name):
        l_xml = p_xml.find(p_name)
        if l_xml == None:
            l_xml = p_xml.get(p_name)
        else:
            l_xml = l_xml.text
        return str(l_xml)

    def put_text_attribute(self, p_element, p_name, p_text):
        try:
            l_var = str(p_text)
        except (ValueError, TypeError):
            l_var = ''
        p_element.set(p_name, l_var)

    def put_text_element(self, p_parent_element, p_name, p_text):
        try:
            l_var = str(p_text)
        except (ValueError, TypeError):
            l_var = ''
        ET.SubElement(p_parent_element, p_name).text = l_var

#-----
# UUID
#-----
    def get_uuid_from_xml(self, p_xml, p_name):
        """Always return an UUID - generate one if it is missing.
        """
        l_xml = p_xml.find(p_name)
        if l_xml == None:
            l_xml = str(p_xml.get(p_name))
        else:
            l_xml = str(l_xml.text)
        if len(l_xml) < 8:
            l_xml = str(uuid.uuid1())
        return l_xml

#-----

    def put_str(self, p_obj):
        try:
            l_var = str(p_obj)
        except AttributeError:
            l_var = 'no str value'
        return l_var


    def put_bool(self, p_arg):
        l_text = 'False'
        if p_arg != False: l_text = 'True'
        return l_text


class ConfigTools(PutGetXML):

    def xml_create_common_element(self, p_title, p_obj):
        """Build a common entry.
        """
        l_elem = ET.Element(p_title)
        l_elem.set('Name', p_obj.Name)
        l_elem.set('Key', str(p_obj.Key))
        l_elem.set('Active', self.put_bool(p_obj.Active))
        return l_elem

    def xml_read_common_info(self, p_obj, p_entry_xml):
        """Get the common (Name, Key, Active) information from an XML sub-tree.

        @param p_obj: is the object we are updating the common information for.
        @param p_entry_xml: is the XML subtree that we are extracting the information from.
        """
        p_obj.Name = self.get_text_from_xml(p_entry_xml, 'Name')
        p_obj.Key = self.get_int_from_xml(p_entry_xml, 'Key')
        p_obj.Active = self.get_bool_from_xml(p_entry_xml, 'Active')


class ConfigFile(PutGetXML):

    m_std_path = '/etc/pyhouse/', '~/.PyHouse/', '/var/PyHouse/'
    m_std_name = 'PyHouse.xml'

    def __init__(self):
        pass

    def create_find_config_dir(self):
        """Check for directory existance.  If not, try creating one.
        If we can't create one, return a failure.

        @return: the path we created or found
        """
        for l_dir in self.m_std_path:
            l_dir = os.path.expanduser(l_dir)
            if os.path.exists(l_dir):
                return l_dir
        for l_dir in self.m_std_path:
            l_dir = os.path.expanduser(l_dir)
            try:
                os.mkdir(l_dir)
                return l_dir
            except OSError:
                pass
        print("Could not create any of the following {0:}".format(self.m_std_path))
        sys.exit(1)

    def find_config_file(self, p_dir):
        """Add a file name to the passed in dir to get the config file.
        """
        l_file_name = os.path.join(p_dir, self.m_std_name)
        try:
            open(l_file_name, mode = 'r')
        except IOError:
            self.create_empty_config_file(l_file_name)
        return l_file_name

    def create_empty_config_file(self, p_name):
        """Create an empty skeleton XML config file.

        @param p_name: the complete path and filename to create.
        """
        l_top = ET.Element('PyHouse')
        l_comment = ET.Comment('Generated by PyHouse {0:}'.format(datetime.datetime.now()))
        l_top.append(l_comment)
        open(os.path.expanduser(p_name), 'w')
        l_nice = prettify(l_top)
        print(l_nice)
        ET.ElementTree(l_top).write(p_name)

    def write_xml_file(self, p_xmltree, p_filename = ''):
        p_xmltree.write(p_filename, xml_declaration = True)


def stuff_new_attrs(p_target, p_data):
    """Put the NEW information from the data object into the target object.
    Preserve any attributes already in the target object.
    """
    l_attrs = filter(lambda aname: not aname.startswith('__'), dir(p_data))
    for l_attr in l_attrs:
        if not hasattr(p_target, l_attr):
            setattr(p_target, l_attr, getattr(p_data, l_attr))

def prettify(p_element):
    """Return a pretty-printed XML string for the Element.

    @param p_element: an element to format as a readable XML tree.
    @return: a string formatted with indentation and newlines.
    """
    rough_string = ET.tostring(p_element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent = "    ")

def open_config_file():
    """Open the PyHouse config xml file.

    If the file is not found, create a skeleton xml file to be populated by the user via the GUI.

    Search in several standard places for the config file;
    if not found create it after checking for read write permissions.

    @return: the open file name
    """
    l_cf = ConfigFile()
    l_dir = l_cf.create_find_config_dir()
    l_file_name = l_cf.find_config_file(l_dir)
    try:
        open(l_file_name, mode = 'r')
    except Exception as e:  # IOError:
        # g_logger.error(" -- Error in open_config_file {0:}".format(e))
        l_file_name = '~/.PyHouse/PyHouse.xml'
        l_file_name = os.path.expanduser(l_file_name)
        ConfigFile().create_empty_config_file(l_file_name)
    return l_file_name

def write_xml_file(p_xmltree, p_filename):
    prettify(p_xmltree)
    l_tree = ET.ElementTree()
    l_tree._setroot(p_xmltree)
    l_tree.write(p_filename, xml_declaration = True)

# ## END
