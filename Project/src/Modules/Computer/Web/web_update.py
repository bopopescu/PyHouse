"""
@name:      PyHouse/Project/src/Modules/Web/web_update.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 21, 2015
@Summary:

"""

__updated__ = '2019-10-31'

# Import system type stuff
import os

# Import PyMh files and modules.
from Modules.Core import logging_pyh as Logger
from Modules.Core.Utilities import json_tools

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = Logger.getLogger('PyHouse.webUpdate  ')


class UpdateElement(athena.LiveElement):
    """ a 'live' webs element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'updateElement.html'))
    jsClass = u'update.UpdateWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getUpdateData(self):
        """ A JS client has requested all the webs information.
        """
        l_obj = self.m_pyhouse_obj.Computer.Web
        l_json = unicode(json_tools.encode_json(l_obj))
        return l_json

    @athena.expose
    def saveUpdateData(self, p_json):
        """A new/changed web is returned.  Process it and update the internal data via ???.py
        """
        l_json = json_tools.decode_json_unicode(p_json)
        # l_obj = UpdateData()
        # l_obj.Port = l_json['Port']
        # self.m_pyhouse_obj.Computer.WebApi.SaveXml(l_obj)

# ## END DBK
