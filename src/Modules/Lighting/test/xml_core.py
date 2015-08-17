"""
@name:      PyHouse/src/Modules/Lighting/test/xml_core.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 22, 2014
@Summary:

NO LONGER USED - REPLACED BY PyHouse/src/Modules/Core/test/xml_device.py

See PyHouse/src/test/xml_data.py for the entire hierarchy.

"""

# Import system type stuff

# Import PyMh files

TESTING_LIGHTING_CORE_COMMENT = "SwitchLink On/Off"
TESTING_LIGHTING_CORE_COORDS = "['0', '0', '0']"
TESTING_LIGHTING_CORE_DIMMABLE = True
TESTING_LIGHTING_CORE_ROOM = "Master Bath"
TESTING_LIGHTING_CORE_INSTEON = "Insteon"
TESTING_LIGHTING_CORE_UPB = "UPB"

CORE_DEVICE = "<Comment>" + TESTING_LIGHTING_CORE_COMMENT + """</Comment>
    <Coords>""" + TESTING_LIGHTING_CORE_COORDS + """</Coords>
    <IsDimmable>""" + str(TESTING_LIGHTING_CORE_DIMMABLE) + """</IsDimmable>
    <RoomName>""" + TESTING_LIGHTING_CORE_ROOM + """</RoomName>
    <ControllerFamily>Insteon</ControllerFamily>"""

# ## END DBK
