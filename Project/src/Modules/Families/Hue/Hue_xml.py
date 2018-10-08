"""
-*- test-case-name: PyHouse/src/Modules/Families/Hue/Hue_xml.py -*-

@name:      PyHouse/src/Modules/Families/Hue/Hue_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@note:      Created on Dec 18, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2018-01-04'

# Import system type stuff

# Import PyMh files
from Modules.Core.Utilities.xml_tools import PutGetXML, stuff_new_attrs
from Modules.Families.Hue.Hue_data import HueAddInData
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Hue_xml    ')


class Xml(object):
    """ bridges_xml calls these when the
    """

    @staticmethod
    def _read_hue(p_in_xml):
        l_hue_obj = HueAddInData()
        l_hue_obj.ApiKey = PutGetXML.get_text_from_xml(p_in_xml, 'ApiKey')
        return l_hue_obj

    @staticmethod
    def _write_hue(p_xml, p_obj):
        """
        """
        PutGetXML.put_text_element(p_xml, 'ApiKey', p_obj.ApiKey)
        return p_xml  # for testing

    @staticmethod
    def ReadXml(p_device_obj, p_entry_xml):
        """
        A method to extract Hue specific elements and insert them into an Bridge data object.

        We do this to keep the Hue Data encapsulated.

        @param p_device_obj : is the Object that will have the extracted elements inserted into.
        @param p_entry_xml: is the device's XML element
        @return: a dict of the extracted Hue Specific data.
        """
        l_hue_obj = Xml._read_hue(p_entry_xml)
        stuff_new_attrs(p_device_obj, l_hue_obj)
        return p_device_obj  # For testing only

    @staticmethod
    def WriteXml(p_xml, p_obj):
        """
        @param p_xml: is a parent element to which the Hue Specific information is appended.
        @param p_obj: is the object for which we are putting the xml
        """
        Xml._write_hue(p_xml, p_obj)
        return p_xml

# ## END DBK