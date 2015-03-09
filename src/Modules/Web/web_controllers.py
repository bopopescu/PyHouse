"""
-*- test-case-name: PyHouse.src.Modules.Web.test.test_web_controllers -*-

@name: PyHouse/src/Modules/Web/web_controllers.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 8, 2013
@summary: Web interface to controllers for the selected house.

"""

# Import system type stuff
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.Core import conversions
from Modules.Web.web_utils import JsonUnicode, GetJSONHouseInfo
from Modules.Drivers import interface
from Modules.Lighting import lighting_controllers
from Modules.Computer import logging_pyh as Logger
from Modules.Families.Insteon import Insteon_utils


# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = Logger.getLogger('PyHouse.webCntlr    ')



class ControllersElement(athena.LiveElement):
    """ a 'live' controllers element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'controllersElement.html'))
    jsClass = u'controllers.ControllersWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj
        if g_debug >= 2:
            print("web_controllers.ControllersElement()")

    @athena.expose
    def getHouseData(self):
        l_house = GetJSONHouseInfo(self.m_pyhouse_obj)
        return l_house

    @athena.expose
    def getInterfaceData(self):
        """ A JS request for interface information has been received from the client.
        """
        l_interfaces = interface.VALID_INTERFACES
        l_obj = {}
        for l_interface in l_interfaces:
            l_name = l_interface + 'Data'
        l_json = JsonUnicode().encode_json(l_obj)
        return unicode(l_json)

    @athena.expose
    def saveControllerData(self, p_json):
        """A new/changed controller is returned.  Process it and update the internal data via controller.py
        """
        l_json = JsonUnicode().decode_json(p_json)
        l_controller_ix = int(l_json['Key'])
        l_delete = l_json['Delete']
        if l_delete:
            try:
                del self.m_pyhouse_obj.House.DeviceOBJs.Controllers[l_controller_ix]
            except AttributeError:
                print("web_controllers - Failed to delete - JSON: {0:}".FORMAT(l_json))
            return
        #
        # Note - we don't want a plain controller here - we want a family controller with the proper interface.
        #
        try:
            l_obj = self.m_pyhouse_obj.House.DeviceOBJs.Controllers[l_controller_ix]
        except KeyError:
            l_obj = lighting_controllers.ControllerData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_controller_ix
        l_obj.Comment = l_json['Comment']
        l_obj.Coords = l_json['Coords']
        l_obj.IsDimmable = l_json['IsDimmable']
        l_obj.ControllerFamily = l_json['ControllerFamily']
        l_obj.RoomName = l_json['RoomName']
        l_obj.LightingType = l_json['LightingType']
        l_obj.UUID = l_json['UUID']
        l_obj.InterfaceType = l_json['InterfaceType']
        l_obj.Port = l_json['Port']
        if l_obj.ControllerFamily == 'Insteon':
            Insteon_utils.Util().get_jaon_data(l_obj, l_json)
        elif l_obj.ControllerFamily == 'UPB':
            l_obj.UPBAddress = l_json['UPBAddress']
            l_obj.UPBPassword = l_json['UPBPassword']
            l_obj.UPBNetworkID = l_json['UPBNetworkID']
        if l_obj.InterfaceType == 'Serial':
            l_obj.BaudRate = l_json['BaudRate']
        self.m_pyhouse_obj.House.DeviceOBJs.Controllers[l_controller_ix] = l_obj
        LOG.info('Controller Added - {}'.format(l_obj))

# ## END DBK
