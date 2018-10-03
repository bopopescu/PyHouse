"""
-*- test-case-name: /home/briank/workspace/PyHouse/src/Modules/Computer/Mqtt/mqtt_data.py -*-

@name:      /home/briank/workspace/PyHouse/src/Modules/Computer/Mqtt/mqtt_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@note:      Created on Feb 11, 2018
@license:   MIT License
@summary:

"""

__updated__ = '2018-10-01'

#  Import system type stuff

#  Import PyMh files
from Modules.Core.data_objects import BaseObject


class MqttInformation(object):
    """

    ==> PyHouse.Computer.Mqtt.xxx as in the def below
    """

    def __init__(self):
        self.Brokers = {}  # MqttBrokerData()
        self.ClientID = 'PyH-'
        self.Prefix = ''


class MqttBrokerData(BaseObject):
    """ 0-N

    ==> PyHouse.Computer.Mqtt.Brokers.XXX as in the def below
    """

    def __init__(self):
        super(MqttBrokerData, self).__init__()
        self.BrokerAddress = None  # Host name or Address
        self.BrokerPort = None
        self.Class = 'Local'
        self.Keepalive = 60  # seconds
        self.Password = None
        self.UserName = None
        self.WillMessage = ''
        self.WillQoS = 0
        self.WillRetain = False
        self.WillTopic = ''
        #
        self._ClientAPI = None
        self._ProtocolAPI = None
        self._isTLS = False


class MqttJson(object):
    """ This is a couple of pieces of information that get added into every MQTT message
        sent out of this computer.
    """

    def __init__(self):
        self.Sender = ''  # The Mqtt name of the sending device.
        self.DateTime = None  # The time on the sending device

# ## END DBK
