#!/usr/bin/python
'''
Created on May 30, 2013

@author: briank
'''

# Import system type stuff
import logging
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from src.web import web_utils

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# 5 = Detailed Data
# + = NOT USED HERE
g_logger = logging.getLogger('PyHouse.webHMenu')

g_logger = None


class HouseMenuElement(athena.LiveElement):
    """
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'houseMenuElement.html'))
    jsClass = u'houseMenu.HouseMenuWidget'

    def __init__(self, p_workspace_obj):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print "web_houseMenu.houseMenuElement()"

# ## END DBK
