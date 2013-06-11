#!/usr/bin/python

"""Web server module.
This is a Main Module - always present.

TODO: format doc strings to Epydoc standards.
"""

# Import system type stuff
import logging
import os
from twisted.internet import reactor
from nevow import appserver

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web import web_utils
from src.web import web_rootmenu



g_debug = 5
# 0 = off
# 1 = major routine entry
# 2 = Basic data

g_port = 8580
g_logger = None
g_houses_obj = None

SUBMIT = '_submit'
BUTTON = 'post_btn'

# Only to move the eclipse error flags to one small spot
listenTCP = reactor.listenTCP

class WebData(object):
    """
    """
    def __init__(self):
        self.WebPort = 8580


class API(object):

    def __init__(self):
        global g_logger
        g_logger = logging.getLogger('PyHouse.WebServ ')
        self.web_data = WebData()
        if g_debug >= 1:
            print "web_server.API()"
        g_logger.info("Initialized")

    def Start(self, p_pyhouses_obj):
        if g_debug >= 1:
            print "web_server.API.Start()"
        if g_debug >= 2:
            print "    ", p_pyhouses_obj
        self.m_pyhouses_obj = p_pyhouses_obj
        web_utils.WebUtilities().read_xml_config_web(self.web_data, p_pyhouses_obj.XmlRoot)
        l_site_dir = os.path.split(os.path.abspath(__file__))[0]
        l_site = appserver.NevowSite(web_rootmenu.RootPage('/', p_pyhouses_obj))
        listenTCP(self.web_data.WebPort, l_site)
        if g_debug >= 2:
            print "web_server.Start() - Port:{0:}, Path:{1:}".format(self.web_data.WebPort, l_site_dir)
        g_logger.info("Started.")
        return self.web_data

    def Stop(self):
        if g_debug >= 1:
            print "web_server.API.Stop()"

    def Reload(self, p_pyhouses_obj):
        if g_debug >= 1:
            print "web_server.API.Reload()"

# ## END DBK
