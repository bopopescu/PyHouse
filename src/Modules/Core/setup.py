"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_setup -*-

@name: PyHouse/src/Modules/Core/setup.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Mar 1, 2014
@license: MIT License
@summary: This module sets up the Core part of PyHouse.


This will set up this node and then find all other nodes in the same domain (House).

Then start the House and all the sub systems.

Each node has two main sections.
    The first is the Computer part.
    It deals with things that pertain to the computer.

    The second is the house.  This is the main part.
    Every system and sub-system that pertains to the house being automated is here.
"""

# Import system type stuff
import datetime
import xml.etree.ElementTree as ET
from twisted.internet import reactor
from twisted.application.service import Application

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, PyHouseAPIs, \
    TwistedInformation, CoreServicesInformation, XmlInformation, \
    CompAPIs, HouseAPIs
from Modules.Computer import computer
from Modules.Computer import logging_pyh as Logger
from Modules.Housing import house
from Modules.Utilities import xml_tools
from Modules.Utilities.config_file import ConfigAPI
from Modules.Utilities.xml_tools import XmlConfigTools
# from Modules.Utilities.tools import PrettyPrintAny

g_debug = 0
LOG = Logger.getLogger('PyHouse.CoreSetup   ')

INTER_NODE = 'tcp:port=8581'
INTRA_NODE = 'unix:path=/var/run/pyhouse/node:lockfile=1'
INITIAL_DELAY = 2 * 60
REPEAT_DELAY = 2 * 60 * 60  # 2 hours


class ReadWriteConfigXml(XmlConfigTools):
    """Use the internal data to read / write an updated XML config file.
    """

    def read_xml_config_info(self, p_pyhouse_obj):
        """This will read the XML config file(s).
        This puts the XML tree and file name in the pyhouse object for use by various modules.
        """
        l_name = p_pyhouse_obj.Xml.XmlFileName
        try:
            l_xmltree = ET.parse(l_name)
        except (SyntaxError, IOError) as e_error:
            LOG.error('Setup-XML file ERROR - {0:} - {1:}'.format(e_error, l_name))
            ConfigAPI().create_empty_config_file(l_name)
            l_xmltree = ET.parse(p_pyhouse_obj.Xml.XmlFileName)
        p_pyhouse_obj.Xml.XmlRoot = l_xmltree.getroot()


class Utility(ReadWriteConfigXml):
    """
    """

    def log_start(self):
        LOG.info("""
        ------------------------------------------------------------------

        """)

    def load_xml_config_file(self, p_pyhouse_obj):
        # p_pyhouse_obj.Xml.XmlFileName = ConfigAPI().open_config_file(p_pyhouse_obj)
        p_pyhouse_obj.Xml.XmlFileName = '/etc/pyhouse/master.xml'

    def create_empty_xml_skeleton(self):
        l_xml = ET.Element("PyHouse")
        xml_tools.PutGetXML().put_text_attribute(l_xml, 'Version', self.m_pyhouse_obj.Xml.XmlVersion)
        xml_tools.PutGetXML().put_text_attribute(l_xml, 'xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        xml_tools.PutGetXML().put_text_attribute(l_xml, 'xsi:schemaLocation', 'http://PyHouse.org schemas/PyHouse.xsd')
        xml_tools.PutGetXML().put_text_attribute(l_xml, 'xmlns:comp', 'http://PyHouse.Org/ComputerDiv')
        #
        l_xml.append(ET.Comment(' Updated by PyHouse {0:} '.format(datetime.datetime.now())))
        return l_xml

    def _xml_save_loop(self, p_pyhouse_obj):
        self.m_pyhouse_obj.Twisted.Reactor.callLater(REPEAT_DELAY, self._xml_save_loop, p_pyhouse_obj)
        self.WriteXml()

    def create_pyhouse_obj(self, p_parent):
        l_pyhouse_obj = PyHouseData()
        l_pyhouse_obj.APIs = PyHouseAPIs()
        l_pyhouse_obj.APIs.Comp = CompAPIs()
        l_pyhouse_obj.APIs.House = HouseAPIs()
        l_pyhouse_obj.APIs.PyHouseAPI = p_parent  # Only used by web server to reload - Do we need this?
        l_pyhouse_obj.APIs.CoreSetupAPI = self
        l_pyhouse_obj.APIs.Comp.ComputerAPI = computer.API()
        l_pyhouse_obj.APIs.House.HouseAPI = house.API()
        l_pyhouse_obj.Twisted = TwistedInformation()
        l_pyhouse_obj.Twisted.Reactor = reactor
        l_pyhouse_obj.Twisted.Application = Application('PyHouse')
        l_pyhouse_obj.Services = CoreServicesInformation()
        l_pyhouse_obj.Xml = XmlInformation()
        l_pyhouse_obj.Xml.XmlFileName = '/etc/pyhouse/master.xml'
        return l_pyhouse_obj



class API(Utility):

    def Start(self, p_pyhouse_obj):
        """
        The reactor is now running.

        @param p_pyhouse_obj: is the skeleton Obj filled in some by PyHouse.py.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.load_xml_config_file(p_pyhouse_obj)
        self.read_xml_config_info(self.m_pyhouse_obj)
        self.log_start()
        LOG.info("Starting.")
        # Logging system is now enabled
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.APIs.Comp.ComputerAPI.Start(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.HouseAPI.Start(p_pyhouse_obj)
        LOG.info("Started.")
        self.m_pyhouse_obj.Twisted.Reactor.callLater(INITIAL_DELAY, self._xml_save_loop, p_pyhouse_obj)

    def Stop(self):
        self.WriteXml()
        self.m_pyhouse_obj.APIs.Comp.ComputerAPI.Stop()
        self.m_pyhouse_obj.APIs.House.HouseAPI.Stop()
        LOG.info("Stopped.")

    def WriteXml(self):
        """
        Take a snapshot of the current Configuration/Status and write out an XML file.
        """
        # LOG.info("Saving XML.")
        l_xml = self.create_empty_xml_skeleton()
        self.m_pyhouse_obj.APIs.Comp.ComputerAPI.WriteXml(l_xml)
        self.m_pyhouse_obj.APIs.House.HouseAPI.WriteXml(l_xml)
        ConfigAPI().write_xml_config_file(self.m_pyhouse_obj, l_xml, self.m_pyhouse_obj.Xml.XmlFileName)
        LOG.info("Saved XML.")

def load_xml_config():
    pass

# ## END DBK
