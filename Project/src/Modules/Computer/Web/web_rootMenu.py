"""
@name:      PyHouse/Project/src/Modules/Computer/Web/web_rootMenu.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 30, 2013
@summary:   Handle the Main menu.

"""

__updated__ = '2019-10-31'

# Import system type stuff
from twisted.web._element import renderer, Element

# Import PyMh files and modules.
from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.webRootMenu    ')


class RootMenuElement(Element):
    """
    """
    # docFactory = loaders.xmlfile(os.path.join(templatepath, 'rootMenuElement.html'))
    jsClass = u'rootMenu.RootMenuWidget'

    def __init__(self, p_workspace_obj):
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @renderer
    def XXdoRootMenuReload(self, _p_json):
        """ Process a message for a XML save/reload from the browser/client.
        """
        LOG.info("Self: {}".format(self))
        self.m_pyhouse_obj.XXPyHouseMainApi.SaveXml(self.m_pyhouse_obj)

    @renderer
    def doRootMenuQuit(self, p_json):
        """ Process a message for a browser logoff and quit that came from the browser/client.
        """
        LOG.info("Self: {};  JSON: {}".format(self, p_json))

# ## END DBK
