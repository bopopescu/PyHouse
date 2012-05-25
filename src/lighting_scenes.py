#!/usr/bin/env python

"""Handle the scenes component of the lighting system.
"""


Scene_Data = {}

class SceneData(object):
    """
    """

    def __init__(self):
        self.Active = None
        self.Name = None
        self.Light = None
        self.Controller = None
        self.Level = None
        self.Rate = None

    def __repr__(self):
        l_ret = "Scene Name:{0:} - Light:{1:}".format(self.Name, self.Light)
        return l_ret


class SceneAPI(SceneData):
    """
    """

    def load_all_scenes(self, p_dict):
        for l_key, l_value in p_dict.iteritems():
            self.load_scene(l_value)

    def load_scene(self, p_dict):
        l_scene = SceneData()
        Name = l_scene.Active = p_dict.get('Active', None)
        Name = l_scene.Name = p_dict.get('Name', None)
        Scene_Data[Name] = l_scene
        return l_scene

    def dump_all_scenes(self):
        print "***** All Scenes *****"
        for l_key, l_obj in Scene_Data.iteritems():
            print "~~~Scene: {0:}".format(l_key)
            print "     ", l_obj
        print



### END