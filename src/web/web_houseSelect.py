'''
Created on Jun 1, 2013

@author: briank
'''

# Import system type stuff
from nevow import loaders
from nevow import rend

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web import web_utils
from src.web import web_houseMenu


g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 = Basic data


class SelectHousePage(web_utils.ManualFormMixin):
    """
    """
    addSlash = True
    docFactory = loaders.xmlfile('houseSelect.xml', templateDir = 'src/web/template')

    def __init__(self, p_name, p_pyhouses_obj):
        self.m_name = p_name
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 1:
            print "web_houseSelect.SelectHousePage()"
        l_css = ['src/web/css/mainPage.css']
        web_utils.add_attr_list(SelectHousePage, l_css)
        rend.Page.__init__(self)

    def data_houselist(self, _context, _data):
        l_house = {}
        for l_key, l_houses_obj in self.m_pyhouses_obj.HousesData.iteritems():
            l_house[l_key] = l_houses_obj.HouseObject
        return l_house

    def render_action(self, _ctx, _data):
        return web_utils.action_url()

    def render_houselist(self, _context, links):
        l_ret = []
        l_cnt = 0
        for l_key, l_value in sorted(links.iteritems()):
            l_name = l_value.Name
            if l_cnt > 0 and l_cnt % 4 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON)
                         [ l_name])
            l_cnt += 1
        return l_ret

    def form_post_add(self, **kwargs):
        if g_debug >= 2:
            print "web_selecthouse.form_post_add() (HousePage)", kwargs
        return SelectHousePage(self.m_name, self.m_pyhouses_obj)

    def form_post_0(self, **kwargs):
        if g_debug >= 2:
            print "web_selecthouse.form_post_0()", kwargs
        if g_debug >= 5:
            print vars(self.m_pyhouses_obj)
        return web_houseMenu.HouseMenuPage(self.m_name, self.m_pyhouses_obj, 0)

    def form_post_1(self, **kwargs):
        if g_debug >= 2:
            print "web_selecthouse.form_post_1()", kwargs
        return web_houseMenu.HouseMenuPage(self.m_name, self.m_pyhouses_obj, 1)

    def form_post_2(self, **kwargs):
        if g_debug >= 2:
            print "web_selecthouse.form_post_2()", kwargs
        return web_houseMenu.HouseMenuPage(self.m_name, self.m_pyhouses_obj, 2)

    def form_post_3(self, **kwargs):
        if g_debug >= 2:
            print "web_selecthouse.form_post_3()", kwargs
        return web_houseMenu.HouseMenuPage(self.m_name, self.m_pyhouses_obj, 3)

    def form_post_change_house(self, **kwargs):
        if g_debug >= 2:
            print "web_selecthouse.form_post_change_house() (HousePage)", kwargs
        return SelectHousePage(self.m_name, self.m_pyhouses_obj)

    def form_post_deletehouse(self, **kwargs):
        if g_debug >= 2:
            print "web_selecthouse.form_post_deletehouse() (HousePage)", kwargs
        return SelectHousePage(self.m_name, self.m_pyhouses_obj)

    def form_post_house(self, **kwargs):
        if g_debug >= 2:
            print "web_selecthouse.form_post_house() (HousePage)", kwargs
        return SelectHousePage(self.m_name, self.m_pyhouses_obj)

# ## END DBK