'''
Created on May 17, 2013

@author: briank
'''

# Import system type stuff
import logging
import importlib

# Import PyHouse files
from src.families import VALID_FAMILIES


g_debug = 0
# 0 = off
# 1 = major routine entry

g_logger = logging.getLogger('PyHouse.Family  ')
g_family_data = {}


class FamilyData(object):
    """A container for every family that has been defined.
    """

    def __init__(self):
        global ScheduleCount
        self.Active = False
        self.Api = None
        self.ModuleName = ''
        self.Key = 0
        self.ModuleRef = ''
        self.Name = ''
        self.PackageName = ''

    def __repr__(self):
        l_ret = "FamilyData:: "
        l_ret += "Name:{0:}, ".format(self.Name)
        l_ret += "Key:{0:}, ".format(self.Key)
        l_ret += "Active:{0:}, ".format(self.Active)
        l_ret += "Package:{0:}, ".format(self.PackageName)
        l_ret += "Module:{0:}, ".format(self.ModuleName)
        l_ret += "Ref:{0:}, ".format(self.ModuleRef)
        l_ret += "API:{0:}".format(self.Api)
        return l_ret


class LightingUtility(FamilyData):
    """
    """

    def build_lighting_family_info(self, p_house_obj):
        global g_family_data
        l_count = 0
        for l_family in VALID_FAMILIES:
            if g_debug >= 2:
                print "family.build_lighting_family_info - Name: {0:}".format(l_family)
            l_family_obj = FamilyData()
            l_family_obj.Active = False
            l_family_obj.Name = l_family
            l_family_obj.Key = l_count
            l_family_obj.PackageName = 'src.families.' + l_family
            l_family_obj.ModuleName = 'Device_' + l_family
            try:
                l_module = importlib.import_module(l_family_obj.PackageName + '.' + l_family_obj.ModuleName, l_family_obj.PackageName)
            except ImportError:
                if g_debug >= 1:
                    print "    family.build_lighting_family_info() - ERROR - Cannot import module {0:}".format(l_family_obj.ModuleName)
                l_module = None
            l_family_obj.ModuleRef = l_module
            try:
                l_family_obj.Api = l_module.API(p_house_obj)
            except AttributeError:
                if g_debug >= 1:
                    print "    family.build_lighting_family_info() - ERROR - NO API"
                l_family_obj.Api = None
            g_family_data[l_count] = l_family_obj
            if g_debug >= 2:
                # print "family.build_lighting_family_info - PackageName: {0:}, ModuleName: {1:}".format(l_family_obj.PackageName, l_family_obj.ModuleName)
                print "   from {0:} import {1:}".format(l_family_obj.PackageName, l_family_obj.ModuleName)
                print "   g_family_data  Key:{0:} -".format(l_count), l_family_obj
            l_count += 1

    def start_lighting_families(self, p_house_obj):
        """Load and start the family if there is a controller in the house for the family.
        Runs Device_<family>.API.Start()
        """
        if g_debug >= 2:
            print "family.start_lighting_families()"
        g_logger.info("Starting lighting families.")
        for l_family_obj in g_family_data.itervalues():
            if g_debug >= 3:
                print "family.start_lighting_families() - Starting {0:}".format(l_family_obj.Name), l_family_obj
            l_family_obj.Api.Start(p_house_obj)  # will run Device_<family>.API.Start()
            g_logger.info("Started lighting family {0:}.".format(l_family_obj.Name))

    def stop_lighting_families(self, p_xml):
        if g_debug > 1:
            print "family.stop_lighting_families()"
        for l_family_obj in g_family_data.itervalues():
            l_family_obj.Api.Stop(p_xml)

# ## END DBK
