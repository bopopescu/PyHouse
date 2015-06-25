"""
-*- test-case-name: PyHouse.Modules.Computer.Mqtt.test.test_computer -*-

@name:      PyHouse/src/Modules/Computer/Mqtt/mqtt_client.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@Copyright: (c) 2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 5, 2015
@Summary:

"""

# Import system type stuff
import copy

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData
from Modules.Computer import logging_pyh as Logger
from Modules.Computer.Mqtt import mqtt_xml, protocol
from Modules.Web import web_utils


LOG = Logger.getLogger('PyHouse.MqttBroker     ')


class Util(object):
    """
    """

    def __init__(self):
        self.m_connection = None

    def mqtt_start(self, p_pyhouse_obj):
        """ Start the async connection process.

        This is the twisted part.
        The connection of the MQTT protocol is kicked off after the TCP connection is complete.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.Computer.Mqtt.ClientAPI = self
        l_address = p_pyhouse_obj.Computer.Mqtt.BrokerAddress
        l_port = p_pyhouse_obj.Computer.Mqtt.BrokerPort
        print("About to connect to {} {}".format(l_address, l_port))
        p_pyhouse_obj.Twisted.Reactor.connectTCP(l_address, l_port, protocol.MqttClientFactory(p_pyhouse_obj, "DBK1", self))


class API(Util):
    """This interfaces to all of PyHouse.
    """

    m_pyhouse_obj = None
    m_client = None

    def Start(self, p_pyhouse_obj):
        p_pyhouse_obj.Computer.Mqtt.ClientAPI = self
        p_pyhouse_obj.APIs.Comp.MqttAPI = self
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.Computer.Mqtt = mqtt_xml.ReadWriteConfigXml().read_mqtt_xml(p_pyhouse_obj)
        self.m_mqtt = self.mqtt_start(p_pyhouse_obj)
        LOG.info("Broker Started.")

    def Stop(self):
        pass

    def SaveXml(self, p_xml):
        p_xml.append(mqtt_xml.ReadWriteConfigXml().write_mqtt_xml(self.m_pyhouse_obj))
        LOG.info("Saved XML.")

    def MqttPublish(self, p_topic, p_message):
        """Send a topic, message to the broker for it to distribute to the subscription list

        self.m_pyhouse_obj.APIs.Comp.MqttAPI.MqttPublish("pyhouse/schedule/execute", l_schedule_json)

        """
        # print("Broker MqttPublish {} {}".format(p_topic, p_message))
        try:
            self.m_pyhouse_obj.Computer.Mqtt.ProtocolAPI.publish(p_topic, p_message)
        except AttributeError as e_err:
            LOG.error("Unpublished\n   Error:{}\n   Topic:{}\n   Message:{}".format(e_err, p_topic, p_message))

    def MqttDispatch(self, _p_topic, _p_message):
        """Dispatch a MQTT message according to the topic.
        """
        print("MqttDispatch")
        pass

    def doPyHouseLogin(self, p_client, p_pyhouse_obj):
        """Login to PyHouse via MQTT
        """
        self.m_client = p_client
        try:
            l_node = copy.deepcopy(p_pyhouse_obj.Computer.Nodes[0])
        except KeyError:
            l_node = NodeData()
        l_node.NodeInterfaces = None
        l_json = web_utils.JsonUnicode().encode_json(l_node)
        print("Broker - send initial login.")
        p_client.publish('pyhouse/login/initial', l_json)

# ## END DBK