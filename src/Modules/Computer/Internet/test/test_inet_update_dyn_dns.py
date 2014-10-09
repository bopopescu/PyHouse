"""
@name: PyHouse/src/Modules/Computer/Internet/test/test_inet_update_dyn_dns.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com>
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 27, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    Set up pyhouse_obj and xml element pointers
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test(unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_reactor = self.m_pyhouse_obj.Twisted.Reactor

    def testName(self):
        pass

# ## END DBK