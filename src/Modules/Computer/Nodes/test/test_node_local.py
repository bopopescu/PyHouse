"""
@name:      PyHouse/src/Modules/Core/test/test_node_local.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 29, 2014
@summary:   This module is for testing local node data.

Passed all 9 tests - DBK - 2015-09-13

"""

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

#  Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, NodeInterfaceData
from Modules.Computer.Nodes import nodes_xml
from Modules.Computer.Nodes.node_local import Interfaces
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class FakeNetiface(object):
    """
    """


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the test
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeData()

    def test_01_PyHouse(self):
        #  print(PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse'))
        self.assertNotEqual(self.m_pyhouse_obj.Xml, None)

    def test_02_Data(self):
        self.m_pyhouse_obj.Computer.Nodes = nodes_xml.Xml.read_all_nodes_xml(self.m_pyhouse_obj)
        #  print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'PyHouse Computer'))
        self.assertEqual(len(self.m_pyhouse_obj.Computer.Nodes), 2)


class A2_Netiface(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the test
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeData()

    def test_01_Families(self):
        l_fam = Interfaces._list_families()
        print(PrettyFormatAny.form(l_fam, 'A2-01 - Families', 170))
        pass

    def test_02_Gateways(self):
        l_gate = Interfaces._list_gateways()
        #  print(PrettyFormatAny.form(l_gate, 'A2-02 - Gateways', 170))
        pass

    def test_03_Interfaces(self):
        l_int = Interfaces._list_interfaces()
        #  print(PrettyFormatAny.form(l_int, 'A2-03 - Interfaces', 170))
        pass

    def test_04_Interfaces(self):
        l_int = Interfaces._list_interfaces()
        for l_name in l_int:
            l_ifa = Interfaces._list_ifaddresses(l_name)
            print(PrettyFormatAny.form(l_ifa, 'A2-04 Interface Addresses', 170))
        l_all = Interfaces._get_all_interfaces()
        print(PrettyFormatAny.form(l_int, 'A2-04 Interfaces', 170))
        for l_ix in l_all:
            print('{} {}'.format(l_ix, PrettyFormatAny.form(l_all[l_ix], 'Interface', 170)))
        print(PrettyFormatAny.form(l_all, 'A2-04 Interfaces', 170))
        #  print(PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse'))
        #  self.assertNotEqual(self.m_pyhouse_obj.Xml, None)


class B1_Iface(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_pyhouse_obj.Computer.Nodes = nodes_xml.Xml.read_all_nodes_xml(self.m_pyhouse_obj)
        self.m_node = NodeData()
        self.m_iface_api = Interfaces()

    def test_01_AllIfaceNames(self):
        """ This will be different on different computers

        I don't know how to test the returned list for validity.
        Uncomment the print to see what your computer returned.
        """
        print('B1-01')
        l_names = Interfaces.find_all_interface_names()
        print(PrettyFormatAny.form(l_names, 'B1-01 Names'))
        self.assertGreater(len(l_names), 1)

    def test_02_AddrFamilyName(self):
        """
        We are interested in:
            IPv4 (AF_INET)
            IPv6 (AF_INET6)
            MAC  (AF_LINK)
        """
        l_ret = Interfaces._find_addr_family_name(17)
        print(PrettyFormatAny.form(l_ret, 'B1-02 Address Lists'))
        self.assertEqual(l_ret, 'AF_PACKET')

        l_ret = Interfaces._find_addr_family_name(2)
        print(PrettyFormatAny.form(l_ret, 'B1-02 Address Lists'))
        self.assertEqual(l_ret, 'AF_INET')
        l_ret = Interfaces._find_addr_family_name(23)
        print(PrettyFormatAny.form(l_ret, 'B1-02 Address Lists'))
        self.assertEqual(l_ret, 'AF_INET6')

    def test_03_AddrLists(self):
        """
        I don't know how to test the returned list for validity.
        Uncomment the print to see what your computer returned.
        """
        l_names = Interfaces.find_all_interface_names()
        #  On my laptop: returns 7 interfaces.
        print(PrettyFormatAny.form(l_names, 'Address Lists'))
        l_ret = Interfaces._find_addr_lists(l_names[0])
        print(PrettyFormatAny.form(l_ret, 'Address Lists'))

    def test_04_OneInterfaces(self):
        l_names = Interfaces.find_all_interface_names()
        l_node = Interfaces._get_one_interface(l_names[1])
        print(PrettyFormatAny.form(l_node, 'Node Interfaces'))

    def test_05_AllInterfaces(self):
        l_node = NodeData()
        l_node.NodeInterfaces = Interfaces._get_all_interfaces()
        print(PrettyFormatAny.form(l_node.NodeInterfaces, 'Node Interfaces'))


class C07_Api(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        #  self.m_api = node_local.API()

    def test_02_Start(self):
        #  self.m_api.Start(self.m_pyhouse_obj)
        pass

    def test_03_Stop(self):
        #  self.m_api.Stop()
        pass

#  ## END DBK
