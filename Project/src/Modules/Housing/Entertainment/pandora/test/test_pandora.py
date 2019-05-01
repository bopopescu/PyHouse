"""
@name:      PyHouse/src/Modules/entertain/test/test_pandora.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 22, 2014
@summary:   Test

Passed all 20 tests - DBK - 2019-04-20

"""

__updated__ = '2019-04-20'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.Entertainment.entertainment import API as entertainmentAPI
from Modules.Housing.Entertainment.pandora.pandora import \
    API as pandoraAPI, \
    SECTION, \
    MqttActions, \
    PianoBarProcessControl, \
    PandoraStatusData
from Modules.Housing.Entertainment.pandora.test.xml_pandora import \
    XML_PANDORA_SECTION, \
    TESTING_PANDORA_SECTION, \
    L_PANDORA_SECTION_START, \
    TESTING_PANDORA_SERVICE_NAME_0, \
    TESTING_PANDORA_SERVICE_KEY_0, \
    TESTING_PANDORA_SERVICE_ACTIVE_0
from Modules.Housing.test.xml_housing import \
    TESTING_HOUSE_DIVISION, \
    TESTING_HOUSE_NAME, \
    TESTING_HOUSE_ACTIVE, \
    TESTING_HOUSE_KEY, \
    TESTING_HOUSE_UUID
from Modules.Housing.Entertainment.entertainment_data import \
    EntertainmentPluginData
from Modules.Housing.Entertainment.test.xml_entertainment import \
    TESTING_ENTERTAINMENT_SECTION
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

CTL = {
    'Sender' : 'Computer_1',
    'Control': 'PowerOff'
    }

TIME_LN = b'#   -03:00/03:00\r'
PLAY_LN = b'   "Love Is On The Way" by "Dave Koz" on "Greatest Hits" <3 @ Smooth Jazz Radio'


class SetupMixin:

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):
    """ Prints the test ID
    """

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_pandora')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up pyhouse_obj and the XML tags that we will need
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly.
        """
        l_xml = self.m_xml.entertainment_sect
        # print(PrettyFormatAny.form(l_xml, 'A1-01-A - Entertainment XML'))
        self.assertIsNotNone(l_xml.find(TESTING_PANDORA_SECTION))

    def test_02_XmlTags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-02-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.entertainment_sect.tag, TESTING_ENTERTAINMENT_SECTION)
        self.assertEqual(self.m_xml.pandora_sect.tag, TESTING_PANDORA_SECTION)


class A2_SetupXml(SetupMixin, unittest.TestCase):
    """ Test that the XML contains no syntax errors.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))

    def test_01_Raw(self):
        l_raw = XML_PANDORA_SECTION
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:16], L_PANDORA_SECTION_START[:16])

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_PANDORA_SECTION)
        # print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'A2-02-A - Parsed')))
        self.assertEqual(l_xml.tag, TESTING_PANDORA_SECTION)


class A3_XML(SetupMixin, unittest.TestCase):
    """ Now we test that the xml_xxxxx have set up the XML_LONG tree properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_HouseDivXml(self):
        """ Test
        """
        l_xml = self.m_xml.house_div
        # print(PrettyFormatAny.form(l_xml, 'A3-01-A - House'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_HOUSE_NAME)
        self.assertEqual(l_xml.attrib['Active'], TESTING_HOUSE_ACTIVE)
        self.assertEqual(l_xml.attrib['Key'], TESTING_HOUSE_KEY)
        self.assertEqual(l_xml.find('UUID').text, TESTING_HOUSE_UUID)

    def test_02_EntertainmentXml(self):
        """ Test if the number of sub sections is the same as configured in the XML
        """
        l_xml = self.m_xml.entertainment_sect
        # print(PrettyFormatAny.form(l_xml, 'A3-02-A - Entertainment'))
        self.assertGreater(len(l_xml), 0)

    def test_03_PandoraXml(self):
        """ Test
        """
        l_xml = self.m_xml.pandora_sect
        # print(PrettyFormatAny.form(l_xml, 'A3-03-A - Pandora'))
        self.assertEqual(len(l_xml), 3)
        self.assertEqual(l_xml[2].attrib['Name'], TESTING_PANDORA_SERVICE_NAME_0)

    def test_04_Service0(self):
        """ Be sure that the XML contains everything in RoomData().
        """
        l_xml = self.m_xml.pandora_sect.find('Service')
        # print(PrettyFormatAny.form(l_xml, 'A3-04-A Device'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_PANDORA_SERVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_PANDORA_SERVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_PANDORA_SERVICE_ACTIVE_0)


class E1_API(SetupMixin, unittest.TestCase):
    """ Test that we are initializing properly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)

    def test_01_Init(self):
        """ Test that the data structure is correct.
        """
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION], 'E1-01-D - Section', 180))
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        self.assertIsNone(l_base._API)
        self.assertEqual(l_base.Active, False)
        self.assertEqual(l_base.ServiceCount, 0)


class E2_API(SetupMixin, unittest.TestCase):
    """ Test that we write XML correctly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()

        # self.m_xml_pandora = self.m_xml.entertainment_sect.find('PandoraSection').find('Device')
        # self.m_pandora = pandoraXml.read_pandora_section_xml(self.m_pyhouse_obj)

    def test_02_Load(self):
        """ Test that the data structure is correct.
        """
        self.m_api.LoadXml(self.m_pyhouse_obj)
        l_pandora_sect = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        # print(PrettyFormatAny.form(l_pandora_sect, 'E2-02-A - Section', 180))
        # print(PrettyFormatAny.form(l_pandora_sect.Services, 'E2-02-A - Section', 180))
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        self.assertEqual(l_base.Active, True)
        self.assertEqual(l_base.ServiceCount, 1)


class E3_API(SetupMixin, unittest.TestCase):
    """ Test that we write XML correctly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_api.LoadXml(self.m_pyhouse_obj)

    def test_03_Start(self):
        """ Test that the data structure is correct.
        """
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]

    def test_04_Save(self):
        """ Test that the data structure is correct.
        """
        l_xml = ET.Element('EntertainmentSection')
        l_section = self.m_api.SaveXml(l_xml)
        # print(PrettyFormatAny.form(l_section, 'E3-04-A - Section'))

    def test_05_Stop(self):
        """ Test that the data structure is correct.
        """
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]


class F1_Mqtt(SetupMixin, unittest.TestCase):
    """ Test that we handle messages properly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_api.LoadXml(self.m_pyhouse_obj)
        self.m_mqtt = MqttActions(self.m_pyhouse_obj)

    def test_01_Decode(self):
        """ Test that the data structure is correct.
        """
        l_topic = ['control']
        l_message = 'X'
        # l_log = self.m_api.decode(l_topic, CTL)
        # print(l_log)

    def test_02_Control(self):
        """ Test that the data structure is correct.
        """
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]


class F2_Extract(SetupMixin, unittest.TestCase):
    """ Test that we handle messages properly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_api.LoadXml(self.m_pyhouse_obj)

    def test_01_Time(self):
        """ Test that the data structure is correct.
        """
        l_obj = PandoraStatusData()
        l_res = PianoBarProcessControl(self.m_pyhouse_obj)._extract_playtime(l_obj, TIME_LN)
        # print(PrettyFormatAny.form(l_obj, 'F2-01-A - Status', 180))
        self.assertEqual(l_res.PlayingTime, '03:00')

    def test_02_Line(self):
        """ Test that the data structure is correct.
        """
        l_obj = PandoraStatusData()
        l_res = PianoBarProcessControl(self.m_pyhouse_obj)._extract_nowplaying(l_obj, PLAY_LN)
        # print(PrettyFormatAny.form(l_obj, 'F2-02-A - Status', 180))
        self.assertEqual(l_res.Album, 'Greatest Hits')
        self.assertEqual(l_res.Artist, 'Dave Koz')
        self.assertEqual(l_res.Likability, '3')
        self.assertEqual(l_res.Song, 'Love Is On The Way')
        self.assertEqual(l_res.Station, 'Smooth Jazz Radio')


class G1_Extract(SetupMixin, unittest.TestCase):
    """ Test that we handle messages properly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_api.LoadXml(self.m_pyhouse_obj)


class G2_Extract(SetupMixin, unittest.TestCase):
    """ Test that we handle messages properly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_api.LoadXml(self.m_pyhouse_obj)

# ## END DBK
