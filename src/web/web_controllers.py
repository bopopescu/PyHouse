'''
Created on Apr 8, 2013

@author: briank
'''

# Import system type stuff
from nevow import loaders
from nevow import rend
from nevow import static
import json

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web import web_utils


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Dump JSON
# + = NOT USED HERE


class ControllersPage(web_utils.ManualFormMixin):
    """Define the page layout of the lighting selection web page.
    """
    addSlash = True
    docFactory = loaders.stan(
        T_html["\n",
            T_head["\n",
                T_title['PyHouse - Lighting Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js'),
                T_script(type = 'text/javascript', src = 'controllerspage.js')["\n"],
                ],
            T_body[
                T_h1['PyHouse Controllers'],
                T_p['Select the controller:'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    T_invisible(data = T_directive('controllerslist'), render = T_directive('controllerslist'))
                    ],
                T_form(action = U_H_child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post'
                      )["\n",
                    T_input(type = 'button', onclick = "createNewControllerWindow('1234')", value = 'Add Controller')
                    ]  # form
                ]  # body
            ]  # html
        )  # stan

    def __init__(self, p_parent, p_name, p_house_obj):
        self.m_name = p_name
        self.m_parent = p_parent
        self.m_house_obj = p_house_obj
        if g_debug >= 2:
            print "web_controllers.ControllersPage()"
        rend.Page.__init__(self)
        setattr(ControllersPage, 'child_lightpage.css', static.File('web/css/lightpage.css'))
        setattr(ButtonsPage, 'child_mainpage.css', static.File('web/css/mainpage.css'))
        setattr(ButtonsPage, 'child_ajax.js', static.File('web/js/ajax.js'))
        setattr(ButtonsPage, 'child_floating_window.js', static.File('web/js/floating-window.js'))
        setattr(ButtonsPage, 'child_controllerspage.js', static.File('web/js/controllerspage.js'))
        #------------------------------------
        setattr(ButtonsPage, 'child_bottomRight.gif', static.File('web/images/bottom_right.gif'))
        setattr(ButtonsPage, 'child_close.gif', static.File('web/images/close.gif'))
        setattr(ButtonsPage, 'child_minimize.gif', static.File('web/images/minimize.gif'))
        setattr(ButtonsPage, 'child_topCenter.gif', static.File('web/images/top_center.gif'))
        setattr(ControllersPage, 'child_topLeft.gif', static.File('web/images/top_left.gif'))
        setattr(ControllersPage, 'child_topRight.gif', static.File('web/images/top_right.gif'))
        setattr(ButtonsPage, 'child_handle.horizontal.png', static.File('web/images/handle.horizontal.png'))

    def data_controllerslist(self, _context, _data):
        """Build up a list of controllers.
        """
        if g_debug >= 2:
            print "web_controllers.data_controllerslist()"
        l_controller = {}
        for l_key, l_obj in self.m_house_obj.Controllers.iteritems():
            l_controller[l_key] = l_obj
        return l_controller

    def render_controllerslist(self, _context, links):
        """Place buttons for each light on the page.
        """
        if g_debug >= 2:
            print "web_controllers.render_controllerslist()"
        l_ret = []
        l_cnt = 0
        for l_key, l_obj in sorted(links.iteritems()):
            l_json = json.dumps(repr(l_obj))
            if g_debug >= 4:
                print "    json = ", l_json
                print "    vars = ", vars(l_obj)
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON,
                    onclick = "createChangeControllerWindow({0:})".format(l_json))
                         [ l_obj.Name])
            l_cnt += 1
        return l_ret

    def _store_controller(self, **kwargs):
        """Send the updated lighting info back to the lighting module.
        Update the lighting page with the new information.
        """
        global Lights
        l_name = kwargs['Name']
        Lights[l_name] = {}
        Lights[l_name]['Address'] = kwargs['Address']
        Lights[l_name]['Family'] = kwargs['Family']
        Lights[l_name]['Type'] = kwargs['Type']
        Lights[l_name]['Controller'] = kwargs['Controller']
        Lights[l_name]['Dimmable'] = kwargs['Dimmable']
        Lights[l_name]['Coords'] = kwargs['Coords']
        Lights[l_name]['Master'] = kwargs['Master']
        # lighting.LightingUtility().update_all_lighting_families()

    def form_post_addlight(self, **kwargs):
        print " - form_post_addlight - ", kwargs
        self._store_light(**kwargs)
        return ButtonsPage(self.m_name, self.m_house_obj)

    def form_post_changelight(self, **kwargs):
        """Browser user changed a light (on/off/dim)
        Now send the change to the light.
        """
        print " - form_post_changelight - kwargs=", kwargs
        return ButtonsPage(self.m_name, self.m_house_obj)

    def form_post_deletelight(self, **kwargs):
        print " - form_post_delete - ", kwargs
        del Lights[kwargs['Name']]
        # lighting.LightingUtility().update_all_lighting_families()
        return ButtonsPage(self.m_name, self.m_house_obj)

    def form_post_scan(self, **kwargs):
        """Trigger a scan of all lights and then update light info.
        """
        print " - form_post_scan- ", kwargs
        return ButtonsPage(self.m_name, self.m_house_obj)

    def form_post_lighting(self, **kwargs):
        print " - form_post_lighting - ", kwargs
        return ControllersPage(self.m_name, self.m_house_obj)

# ## END DBK
