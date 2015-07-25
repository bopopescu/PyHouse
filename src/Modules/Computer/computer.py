"""
-*- test-case-name: PyHouse.src.Modules.Computer.test.test_computer -*-

@name:      PyHouse/src/Modules/computer/computer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@note:      Created on Jun 24, 2014
@license:   MIT License
@summary:   Handle the computer information.

This handles the Computer part of the node.  (The other part is "house").

This takes care of starting all the computer modules (In Order).
    Logging
    Mqtt Broker(s)
    Nodes
    Internet Connection(s)
    Web Server(s)
"""

# Import system type stuff
from xml.etree import ElementTree as ET
import platform

# Import PyHouse files
from Modules.Core.data_objects import ComputerAPIs, ComputerInformation
from Modules.Computer import logging_pyh as Logger
from Modules.Communication.communication import API as communicationAPI
from Modules.Communication.send_email import API as emailAPI
from Modules.Computer.Internet.internet import API as internetAPI
from Modules.Computer.Mqtt.mqtt_client import API as mqttAPI
from Modules.Computer.Nodes.nodes import API as nodesAPI
from Modules.Computer.weather import API as weatherAPI
from Modules.Web.web import API as webAPI
from Modules.Utilities.xml_tools import XmlConfigTools

LOG = Logger.getLogger('PyHouse.Computer       ')
DIVISION = 'ComputerDivision'

MODULES = ['Communication', 'Email', 'Internet' , 'Mqtt', 'Node', 'Weather', 'Web']


class ReadWriteConfigXml(XmlConfigTools):
    """
    """

    def read_computer_xml(self, p_pyhouse_obj):
        l_xml = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
        return l_xml

    def write_computer_xml(self, p_pyhouse_obj):
        p_pyhouse_obj.Computer.Name = platform.node()
        p_pyhouse_obj.Computer.Key = 0
        p_pyhouse_obj.Computer.Active = True
        l_xml = XmlConfigTools.write_base_object_xml(DIVISION, p_pyhouse_obj.Computer)
        return l_xml


class Utility(ReadWriteConfigXml):

    m_pyhouse_obj = None

    @staticmethod
    def _init_component_apis(p_pyhouse_obj, p_api):
        """
        Initialize all the computer APIs
        """
        p_pyhouse_obj.APIs.Computer = ComputerAPIs()
        p_pyhouse_obj.APIs.Computer.ComputerAPI = p_api
        p_pyhouse_obj.APIs.Computer.CommunicationsAPI = communicationAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.EmailAPI = emailAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.InternetAPI = internetAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.MqttAPI = mqttAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.NodesAPI = nodesAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.WeatherAPI = weatherAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.WebAPI = webAPI(p_pyhouse_obj)

    @staticmethod
    def _start_component_apis(p_pyhouse_obj):
        p_pyhouse_obj.APIs.Computer.CommunicationsAPI.Start()
        p_pyhouse_obj.APIs.Computer.EmailAPI.Start()
        p_pyhouse_obj.APIs.Computer.InternetAPI.Start()
        p_pyhouse_obj.APIs.Computer.MqttAPI.Start()
        p_pyhouse_obj.APIs.Computer.NodesAPI.Start()
        p_pyhouse_obj.APIs.Computer.WeatherAPI.Start()
        p_pyhouse_obj.APIs.Computer.WebAPI.Start()

    @staticmethod
    def _stop_component_apis(p_pyhouse_obj):
        p_pyhouse_obj.APIs.Computer.CommunicationsAPI.Stop()
        p_pyhouse_obj.APIs.Computer.EmailAPI.Stop()
        p_pyhouse_obj.APIs.Computer.InternetAPI.Stop()
        p_pyhouse_obj.APIs.Computer.MqttAPI.Stop()
        p_pyhouse_obj.APIs.Computer.NodesAPI.Stop()
        p_pyhouse_obj.APIs.Computer.WeatherAPI.Stopl()
        p_pyhouse_obj.APIs.Computer.WebAPI.Stop()

    @staticmethod
    def _save_component_apis(p_pyhouse_obj, p_xml):
        p_pyhouse_obj.APIs.Computer.CommunicationsAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.Computer.EmailAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.Computer.InternetAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.Computer.MqttAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.Computer.NodesAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.Computer.WeatherAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.Computer.WebAPI.SaveXml(p_xml)
        return p_xml


class API(Utility):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        Utility._init_component_apis(p_pyhouse_obj, self)
        p_pyhouse_obj.Computer = ComputerInformation()
        p_pyhouse_obj.Computer.Name = platform.node()

    def Start(self):
        """
        Start processing
        """
        LOG.info('Starting')
        self.read_computer_xml(self.m_pyhouse_obj)
        Utility._start_component_apis(self.m_pyhouse_obj)
        LOG.info('Started')

    def Stop(self):
        """
        Append the house XML to the passed in xlm tree.
        """
        Utility._stop_component_apis(self.m_pyhouse_obj)
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        """
        Take a snapshot of the current Configuration/Status and write out an XML file.
        """
        l_xml = self.write_computer_xml(self.m_pyhouse_obj)
        Utility._save_component_apis(self.m_pyhouse_obj, l_xml)
        p_xml.append(l_xml)
        LOG.info("Saved Computer XML.")
        return p_xml

# ## END DBK
