"""
-*- test-case-name: PyHouse.src.Modules.Web.test.test_web_utils -*-

@name:      PyHouse/src/Modules/Web/web_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 30, 2013
@summary:   Test handling the information for a house.

"""

# Import system type stuff
import jsonpickle
import json

# Import PyMh files and modules.
from Modules.Core.data_objects import JsonHouseData
from Modules.Computer import logging_pyh as Logger


g_debug = 0
LOG = Logger.getLogger('PyHouse.webUtils       ')

# Web States defined
#-------------------
WS_IDLE = 0  # Starting state
WS_LOGGED_IN = 1  # Successful login completed
WS_ROOTMENU = 2
WS_HOUSE_SELECTED = 3
# global things
WS_SERVER = 101
WS_LOGS = 102
# House things
WS_HOUSE = 201
WS_LOCATION = 202
WS_ROOMS = 203
WS_INTERNET = 204
# Light things
WS_BUTTONS = 501
WS_CONTROLLERS = 502
WS_LIGHTS = 503



class UtilJson(object):
    """
    """

    @staticmethod
    def _getHouseBase(p_pyhouse_obj):
        l_ret = JsonHouseData()
        l_ret.Name = p_pyhouse_obj.House.Name
        l_ret.Key = p_pyhouse_obj.House.Key
        l_ret.Active = p_pyhouse_obj.House.Active
        return l_ret


    @staticmethod
    def _get_LocRoom(p_pyhouse_obj, p_ret):
        p_ret.Location = p_pyhouse_obj.House.Location
        p_ret.Rooms = p_pyhouse_obj.House.Rooms


    @staticmethod
    def _get_Modules(p_pyhouse_obj, p_ret):
        p_ret.Buttons = p_pyhouse_obj.House.Buttons
        p_ret.Controllers = p_pyhouse_obj.House.Controllers
        p_ret.Lights = p_pyhouse_obj.House.Lights
        p_ret.Schedules = p_pyhouse_obj.House.Schedules
        p_ret.Thermostats = p_pyhouse_obj.House.Thermostats


    @staticmethod
    def _get_AllHouseObjs(p_pyhouse_obj):
        l_ret = UtilJson._getHouseBase(p_pyhouse_obj)
        UtilJson._get_LocRoom(p_pyhouse_obj, l_ret)
        UtilJson._get_Modules(p_pyhouse_obj, l_ret)
        return l_ret



def GetJSONHouseInfo(p_pyhouse_obj):
    """
    Get house info for the browser.

    This is simplified and customized so JSON encoding works.
    """
    l_ret = UtilJson._get_AllHouseObjs(p_pyhouse_obj)
    l_json = unicode(JsonUnicode().encode_json(l_ret))
    return l_json



def GetJSONComputerInfo(p_pyhouse_obj):
    """Get house info for the browser.
    This is simplified and customized so JSON encoding works.

    @param p_house_obj: is the complete information
    """
    l_ret = p_pyhouse_obj.Computer
    l_json = unicode(JsonUnicode().encode_json(l_ret))
    return l_json



class State(object):
    """Used by various web_ modules to keep the state of the web server.
    """
    def __init__(self):
        self.State = WS_IDLE



class JsonUnicode(object):
    """Utilities for handling unicode and json
    """

    def convert_from_unicode(self, p_input):
        """Convert unicode strings to python 2 strings.
        """
        if isinstance(p_input, dict):
            return {self.convert_from_unicode(key): self.convert_from_unicode(value) for key, value in p_input.iteritems()}
        elif isinstance(p_input, list):
            return [self.convert_from_unicode(element) for element in p_input]
        elif isinstance(p_input, unicode):
            return p_input.encode('ascii')
        else:
            return p_input

    def convert_to_unicode(self, p_input):
        if isinstance(p_input, dict):
            return {self.convert_to_unicode(key): self.convert_to_unicode(value) for key, value in p_input.iteritems()}
        elif isinstance(p_input, list):
            return [self.convert_to_unicode(element) for element in p_input]
        elif isinstance(p_input, (int, bool)):
            return unicode(str(p_input), 'iso-8859-1')
        elif isinstance(p_input, unicode):
            return p_input
        else:
            return unicode(p_input, 'iso-8859-1')

    def decode_json(self, p_json):
        """Convert a json object to a python object
        """
        try:
            l_obj = self.convert_from_unicode(json.loads(p_json))
        except (TypeError, ValueError):
            l_obj = None
        return l_obj

    def encode_json(self, p_obj):
        """Convert a python object to a valid json object.
        """
        try:
            l_json = jsonpickle.encode(p_obj, unpicklable = False, max_depth = 5)
        except (TypeError, ValueError) as l_error:
            print('web_utils.encode_json ERROR {0:}'.format(l_error))
            l_json = u'{}'
        return l_json

# ## END DBK
