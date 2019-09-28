"""
@name:      PyHouse/Project/src/Modules/Entertainment/_test/test_entertainment.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 14, 2013
@summary:   Test

Passed all 13 tests - DBK - 2019-03-18

"""

__updated__ = '2019-06-29'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from Modules.Core.Utilities.xml_tools import XmlConfigTools
from Modules.Housing.Entertainment.entertainment import API as entertainmentAPI
from Modules.Housing.Entertainment.entertainment_data import \
        EntertainmentInformation
from Modules.Housing.test.xml_housing import \
        TESTING_HOUSE_DIVISION, \
        TESTING_HOUSE_NAME, \
        TESTING_HOUSE_ACTIVE, \
        TESTING_HOUSE_KEY, \
        TESTING_HOUSE_UUID
from Modules.Housing.Entertainment.test.xml_entertainment import \
        TESTING_ENTERTAINMENT_SECTION, \
        XML_ENTERTAINMENT, \
        L_ENTERTAINMENT_SECTION_START
from Modules.Housing.Entertainment.pandora.test.xml_pandora import \
        TESTING_PANDORA_SECTION
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = entertainmentAPI(self.m_pyhouse_obj)


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_entertainment')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, {})

    def test_02_XmlTags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-02-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.entertainment_sect.tag, TESTING_ENTERTAINMENT_SECTION)
        self.assertEqual(self.m_xml.pandora_sect.tag, TESTING_PANDORA_SECTION)


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_ENTERTAINMENT
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:22], L_ENTERTAINMENT_SECTION_START)

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_ENTERTAINMENT)
        # print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'A2-02-A - Parsed')))
        self.assertEqual(l_xml.tag, TESTING_ENTERTAINMENT_SECTION)


class A3_XML(SetupMixin, unittest.TestCase):
    """ Now we _test that the xml_xxxxx have set up the XML_LONG tree properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouseXML(self):
        """ Test to see if the house XML is built correctly
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Xml.XmlRoot, 'PyHouse'))
        pass

    def test_02_HouseDivXml(self):
        """ Test to see if the house XML is built correctly
        """
        l_xml = self.m_xml.house_div
        # print(PrettyFormatAny.form(l_xml, 'A3-01-A - House'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_HOUSE_NAME)
        self.assertEqual(l_xml.attrib['Active'], TESTING_HOUSE_ACTIVE)
        self.assertEqual(l_xml.attrib['Key'], TESTING_HOUSE_KEY)
        self.assertEqual(l_xml.find('UUID').text, TESTING_HOUSE_UUID)

    def test_03_EntertainmentXml(self):
        """ Test to see if the Entertainment XML is built properly
        """
        l_xml = self.m_xml.entertainment_sect
        # print(PrettyFormatAny.form(l_xml, 'A3-02-A - Entertainment'))
        # print(PrettyFormatAny.form(l_xml[1][0], 'A3-02-B - Entertainment'))
        self.assertEqual(l_xml.tag, TESTING_ENTERTAINMENT_SECTION)
        self.assertGreater(len(l_xml), 2)


class C1_Load(SetupMixin, unittest.TestCase):
    """ This will _test all of the sub modules ability to load their part of the XML file
            and this modules ability to put everything together in the structure
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_xml = XmlConfigTools.find_xml_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection')
        self.m_entertainment_obj = EntertainmentInformation()
        self.m_pyhouse_obj.House.Entertainment = EntertainmentInformation()  # Clear before loading

    def test_01_Setup(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_xml, 'C1-01-A - Entertainment XML'))
        self.assertEqual(self.m_xml.tag, TESTING_ENTERTAINMENT_SECTION)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'C1-01-B - Entertainment'))
        self.assertEqual(self.m_entertainment_obj.Active, False)
        self.assertEqual(self.m_entertainment_obj.PluginCount, 0)
        self.assertEqual(self.m_entertainment_obj.Plugins, {})

    def test_03_XML(self):
        """ Test
        """
        l_ret = self.m_api.LoadConfig(self.m_pyhouse_obj)
        l_entertain = self.m_pyhouse_obj.House.Entertainment
        # print(PrettyFormatAny.form(l_entertain, 'C1-01-A - Entertainment'))
        # print(PrettyFormatAny.form(l_entertain.Plugins, 'C1-01-B- Plugins'))
        # print(PrettyFormatAny.form(l_entertain.Plugins['onkyo'], 'C1-01-C - Plugins["onkyo"]'))
        # print(PrettyFormatAny.form(l_entertain.Plugins['panasonic'], 'C1-01-D - Plugins["panasonic"]'))
        # print(PrettyFormatAny.form(l_entertain.Plugins['pandora'], 'C1-01-E - Plugins["pandora"]'))
        # print(PrettyFormatAny.form(l_entertain.Plugins['pioneer'], 'C1-01-F - Plugins["pioneer"]'))
        # print(PrettyFormatAny.form(l_entertain.Plugins['samsung'], 'C1-01-G - Plugins["samsung"]'))


class D1_Save(SetupMixin, unittest.TestCase):
    """ Test writing of the entertainment XML.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Setup(self):
        """
        """
        l_xml = self.m_xml.entertainment_sect
        # print(PrettyFormatAny.form(l_xml, 'C1-01-A - Entertainment XML'))
        self.assertEqual(l_xml.tag, TESTING_ENTERTAINMENT_SECTION)

    def test_02_XML(self):
        """ Test
        """
        l_ret = entertainmentAPI(self.m_pyhouse_obj).LoadConfig(self.m_pyhouse_obj)
        l_xml = ET.Element('HouseDivision')
        l_xml1 = entertainmentAPI(self.m_pyhouse_obj).SaveXml(l_xml)
        l_ent = self.m_pyhouse_obj.House.Entertainment = l_ret
        # print(PrettyFormatAny.form(l_ret, 'D1-02-A - Ret'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'D1-02-B - HouseInformation()'))
        # print(PrettyFormatAny.form(l_ent, 'D1-02-C - Entertainment'))
        # print(PrettyFormatAny.form(l_ent.Plugins, 'D1-02-D- Plugins'))
        # print(PrettyFormatAny.form(l_ent.Plugins['onkyo'], 'D1-02-Onkyo - Plugins["onkyo"]'))
        # print(PrettyFormatAny.form(l_ent.Plugins['panasonic'], 'D1-02-Panasonic - Plugins["panasonic"]'))
        # print(PrettyFormatAny.form(l_ent.Plugins['pandora'], 'D1-02-Pandora - Plugins["pandora"]'))
        # print(PrettyFormatAny.form(l_ent.Plugins['pioneer'], 'D1-02-Pioneer - Plugins["pioneer"]'))
        # print(PrettyFormatAny.form(l_ent.Plugins['samsung'], 'D1-02-Samsung - Plugins["pioneer"]'))
        # print(PrettyFormatAny.form(l_ent.Plugins['pandora'].API, 'D1-02-H - Plugins["pandora"].API'))

    def test_03_XML(self):
        """ Test
        """
        l_ret = entertainmentAPI(self.m_pyhouse_obj).LoadConfig(self.m_pyhouse_obj)
        l_xml = ET.Element('HouseDivision')
        l_xml1 = entertainmentAPI(self.m_pyhouse_obj).SaveXml(l_xml)
        l_ent = self.m_pyhouse_obj.House.Entertainment = l_ret
        # print(PrettyFormatAny.form(l_ent.Plugins, 'D1-03-A- Plugins'))
        # print(PrettyFormatAny.form(l_ent.Plugins['pandora'], 'D1-03-Pandora - Plugins["pandora"]'))
        # print(PrettyFormatAny.form(l_ent.Plugins['pandora']._API, 'D1-02-H - Plugins["pandora"].API'))

# ## END DBK