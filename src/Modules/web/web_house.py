'''
Created on Jun 3, 2013

@author: briank
'''

# Import system type stuff
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from Modules.web import web_utils
from Modules.housing import house
from Modules.housing import house
from Modules.utils import pyh_log

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
# 0 = off
# 1 = log extra info
# + = NOT USED HERE
LOG = pyh_log.getLogger('PyHouse.webHouse    ')

class HouseElement(athena.LiveElement):
    """ a 'live' house element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'houseElement.html'))
    jsClass = u'house.HouseWidget'

    def __init__(self, p_workspace_obj):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj
        if g_debug >= 2:
            print("web_house.HouseElement()")

    @athena.expose
    def getHouseData(self, p_index):
        """ A JS client has requested all the information for a given house.

        @param p_index: is the house index number.
        """
        l_ix = int(p_index)
        l_house = self.m_pyhouse_obj.HouseData
        if g_debug >= 3:
            print("web_house.getHouseData() - HouseIndex:{0:}".format(p_index))
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_house))
        return l_json

    @athena.expose
    def saveHouseData(self, p_json):
        """House data is returned, so update the house info.
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_house_ix = int(l_json['HouseIx'])
        l_delete = l_json['Delete']
        if l_delete:
            try:
                del self.m_pyhouse_obj.HouseData
            except AttributeError:
                print("web_lights - Failed to delete - JSON: {0:}".format(l_json))
            return
        if l_house_ix == -1:  # adding a new house
            l_house_ix = len(self.m_pyhouse_obj.HouseData)
        try:
            l_obj = self.m_pyhouse_obj.HouseData
        except KeyError:
            l_obj = house.HouseData()
        try:
            self.m_pyhouse_obj.HouseData[l_house_ix] = l_obj
        except AttributeError:
            self.m_pyhouse_obj.HouseData = l_obj
        l_obj.Name = l_json['Name']
        l_obj.Key = int(l_json['Key'])
        l_obj.HouseIx = l_house_ix
        l_obj.Location.Street = l_json['Street']
        l_obj.Location.City = l_json['City']
        l_obj.Location.State = l_json['State']
        l_obj.Location.ZipCode = l_json['ZipCode']
        l_obj.Location.Phone = l_json['Phone']
        l_obj.Location.Latitude = l_json['Latitude']
        l_obj.Location.Longitude = l_json['Longitude']
        l_obj.Location.TimeZone = l_json['TimeZone']
        l_obj.Location.SavingsTime = l_json['SavingsTime']
        self.m_pyhouse_obj.HouseData = l_obj

# ## END DBK
