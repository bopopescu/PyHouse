"""
@name:      PyHouse/src/Modules/Computer/Nodes/nodes_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 15, 2014
@Summary:

"""


# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, NodeInterfaceData
from Modules.Utilities.xml_tools import PutGetXML, XmlConfigTools
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.Nodes_xml      ')


class Xml(object):

    @staticmethod
    def _read_one_interface_xml(p_interface_element):
        l_interface_obj = NodeInterfaceData()
        XmlConfigTools.read_base_object_xml(l_interface_obj, p_interface_element)
        l_interface_obj.MacAddress = PutGetXML.get_text_from_xml(p_interface_element, 'MacAddress')
        l_interface_obj.V4Address = PutGetXML.get_text_from_xml(p_interface_element, 'IPv4Address')
        l_interface_obj.V6Address = PutGetXML.get_text_from_xml(p_interface_element, 'IPv6Address')
        return l_interface_obj

    @staticmethod
    def _read_interfaces_xml(p_interfaces_xml):
        l_count = 0
        l_ret = {}
        try:
            for l_node_xml in p_interfaces_xml.iterfind('Interface'):
                l_node = Xml._read_one_interface_xml(l_node_xml)
                l_ret[l_count] = l_node
                l_count += 1
        except AttributeError:
            l_ret = {}
        # LOG.info("XML Loaded")
        return l_ret

    @staticmethod
    def _read_one_node_xml(p_node_xml):
        """
        Read the existing XML file (if it exists) and get the node info.
        """
        l_node_obj = NodeData()
        XmlConfigTools.read_base_object_xml(l_node_obj, p_node_xml)
        l_node_obj.ConnectionAddr_IPv4 = PutGetXML.get_text_from_xml(p_node_xml, 'ConnectionAddressV4')
        l_node_obj.ConnectionAddr_IPv6 = PutGetXML.get_text_from_xml(p_node_xml, 'ConnectionAddressV6')
        l_node_obj.NodeRole = PutGetXML.get_int_from_xml(p_node_xml, 'NodeRole')
        try:
            l_node_obj.NodeInterfaces = Xml._read_interfaces_xml(p_node_xml.find('InterfaceSection'))
        except AttributeError as e_err:
            LOG.error('ERROR OneNodeRead error {}'.format(e_err))
        return l_node_obj

    @staticmethod
    def read_all_nodes_xml(p_pyhouse_obj):
        l_comp = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
        l_count = 0
        l_ret = {}
        try:
            l_xml = l_comp.find('NodeSection')
            for l_node_xml in l_xml.iterfind('Node'):
                l_node = Xml._read_one_node_xml(l_node_xml)
                l_ret[l_count] = l_node
                l_count += 1
        except AttributeError as e_err:
            l_ret[0] = NodeData()  # Create an empty Nodes[0]
            LOG.error('ERROR - Node read error - {}'.format(e_err))
        LOG.info('Stored {} Nodes'.format(l_count))
        return l_ret


    @staticmethod
    def _write_one_interface_xml(p_interface_obj):
        l_entry = XmlConfigTools.write_base_object_xml('Interface', p_interface_obj)
        PutGetXML.put_text_element(l_entry, 'MacAddress', p_interface_obj.MacAddress)
        PutGetXML.put_text_element(l_entry, 'IPv4Address', p_interface_obj.V4Address)
        PutGetXML.put_text_element(l_entry, 'IPv6Address', p_interface_obj.V6Address)
        return l_entry

    @staticmethod
    def _write_interfaces_xml(p_interfaces_obj):
        l_xml = ET.Element('InterfaceSection')
        l_count = 0
        for l_interface_obj in p_interfaces_obj.itervalues():
            l_entry = Xml._write_one_interface_xml(l_interface_obj)
            l_xml.append(l_entry)
            l_count += 1
        return l_xml

    @staticmethod
    def _write_one_node_xml(p_node_obj):
        l_entry = XmlConfigTools.write_base_object_xml('Node', p_node_obj)
        PutGetXML.put_text_element(l_entry, 'ConnectionAddressV4', p_node_obj.ConnectionAddr_IPv4)
        PutGetXML.put_text_element(l_entry, 'ConnectionAddressV6', p_node_obj.ConnectionAddr_IPv6)
        PutGetXML.put_int_element(l_entry, 'NodeRole', p_node_obj.NodeRole)
        l_entry.append(Xml._write_interfaces_xml(p_node_obj.NodeInterfaces))
        return l_entry

    @staticmethod
    def write_nodes_xml(p_nodes_obj):
        l_xml = ET.Element('NodeSection')
        l_count = 0
        try:
            for l_node_obj in p_nodes_obj.itervalues():
                # print(PrettyFormatAny.form(l_node_obj, 'Node'))
                l_node_obj.Key = l_count
                l_entry = Xml._write_one_node_xml(l_node_obj)
                l_xml.append(l_entry)
                l_count += 1
        except AttributeError as e_err:
            LOG.error('Error {}'.format(e_err))
        return l_xml

# ## END DBK
