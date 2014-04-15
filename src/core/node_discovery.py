"""
@name: PyHouse/src/core/node_discovery.py

# -*- test-case-name: PyHouse.src.core.test.test_node_discovery -*-

Created on Apr 5, 2014

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License

@summary: This module is for discovering all the PyHouse nodes in a domain.

This Module:
    Uses IPv4 multicast to discover the other PyHouse nodes in the local network
    Uses IPv6 multicast to discover nodes and overrides IPv4 contact info.
    Uses neighbor discovery to find other potential devices that may play a part in home automation.
"""

# Import system type stuff
import logging

from twisted.application import service
from twisted.internet.protocol import DatagramProtocol, ConnectedDatagramProtocol

g_debug = 0
g_logger = logging.getLogger('PyHouse.NodeDiscovry')


__all__ = [
           'API']

PYHOUSE_MULTICAST = '234.35.36.37'
AMP_PORT = 8581
PYHOUSE_DISCOVERY_PORT = 8582
WHOS_THERE = "Who's There?"
I_AM = "I am."


class NodeData(object):

    def __init__(self):
        self.Name = None
        self.Key = 0
        self.Active = True
        self.HostName = ''
        self.ConnectionAddr = None
        self.Role = 0
        self.Interfaces = {}


class MulticastDiscoveryServerProtocol(DatagramProtocol):
    """Listen for PyHouse nodes and respond to them.
    We should get a packet from ourself and also packets from other nodes that are running.
    """
    m_address_list = []
    m_pyhouses_obj = None

    def __init__(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj

    def startProtocol(self):
        """
        Called after protocol has started listening.
        """
        self.transport.setTTL(2)
        _l_defer = self.transport.joinGroup(PYHOUSE_MULTICAST)

    def datagramReceived(self, p_datagram, p_address):
        """
        @type p_datagram: C{str}
        @param p_datagram: is the contents of the datagram.

        @type p_address: C{tupple) (ipaddr, port)
        @param p_address: is the (IpAddr, Port) of the sender of this datagram (reply to address).
        """
        l_node = NodeData()
        l_node.ConnectionAddr = p_address[0]
        if p_address[0] not in self.m_address_list:
            self.m_address_list.append(p_address[0])
            # g_logger.info("Server Discovery Datagram {0:} received from {1:}".format(repr(p_datagram), repr(p_address)))
        if p_datagram == WHOS_THERE:
            l_str = I_AM + ' ' + self.m_pyhouses_obj.CoreData.Nodes[0].Name
            self.transport.write(l_str, p_address)
            # g_logger.debug("Server replying {0:}".format(l_str))
        elif p_datagram.startswith(I_AM):
            l_node.Name = p_datagram.split(' ')[-1]
            self.save_node_info(l_node)

    def save_node_info(self, p_node):
        l_count = 0
        for l_node in self.m_pyhouses_obj.CoreData.Nodes.itervalues():
            l_count += 1
            if p_node.ConnectionAddr == l_node.ConnectionAddr:
                return
        p_node.Key = l_count
        self.m_pyhouses_obj.CoreData.Nodes[l_count] = p_node
        g_logger.debug("Added node {0:} - {1:}, {2:}".format(l_count, p_node.ConnectionAddr, p_node.Name))


class MulticastDiscoveryClientProtocol(ConnectedDatagramProtocol):
    """Find other PyHouse nodes within range."""
    m_pyhouses_obj = None

    def __init__(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj


    def startProtocol(self):
        """
        Called when the protocol starts up.

        All listeners on the multicast address (including us) will receive this message.
        """
        self.transport.setTTL(2)
        _l_defer = self.transport.joinGroup(PYHOUSE_MULTICAST)
        self.transport.write(WHOS_THERE, (PYHOUSE_MULTICAST, PYHOUSE_DISCOVERY_PORT))

    def datagramReceived(self, p_datagram, p_address):
        if p_datagram == WHOS_THERE and self.m_pyhouses_obj.CoreData.Nodes[0].ConnectionAddr == None:
            self.m_pyhouses_obj.CoreData.Nodes[0].ConnectionAddr = p_address[0]
            # g_logger.info("Client Discovery Datagram {0:} received from {1:}".format(repr(p_datagram), repr(p_address)))
            g_logger.debug("Update node 0 address to {0:}, {1:}".format(p_address[0], p_datagram))
            pass


class Utility(object):

    def start_node_discovery(self, p_pyhouses_obj):
        """Use UDP multicast to discover the other PyHouse nodes that are local.
        Fire the client off again once per hour to re-discover any new nodes
        """
        p_pyhouses_obj.CoreData.DiscoveryService = service.Service()
        p_pyhouses_obj.CoreData.DiscoveryService.setName('NodeDiscovery')
        p_pyhouses_obj.CoreData.DiscoveryService.setServiceParent(p_pyhouses_obj.Application)
        self.m_pyhouses_obj = p_pyhouses_obj
        #
        self._start_discovery_server(p_pyhouses_obj)
        self._start_discovery_client(p_pyhouses_obj)

    def _start_discovery_server(self, p_pyhouses_obj):
        """Use listenMultiple=True so that we can run a server and a client on same node."""
        p_pyhouses_obj.Reactor.listenMulticast(PYHOUSE_DISCOVERY_PORT, MulticastDiscoveryServerProtocol(p_pyhouses_obj), listenMultiple = True)

    def _start_discovery_client(self, p_pyhouses_obj):
        p_pyhouses_obj.Reactor.listenMulticast(PYHOUSE_DISCOVERY_PORT, MulticastDiscoveryClientProtocol(p_pyhouses_obj), listenMultiple = True)


class API(Utility):

    def __init__(self):
        # g_logger.info("Initialized.")
        pass

    def Start(self, p_pyhouses_obj):
        self.start_node_discovery(p_pyhouses_obj)
        # g_logger.info("Started.")

    def Stop(self):
        g_logger.info("Stopped.")

# ## END DBK