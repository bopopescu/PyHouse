"""
@name:      PyHouse/src/Modules/Entertainment/test/xml_entertainment.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 17, 2014
@Summary:

"""

__updated__ = '2016-07-16'

L_ENTERTAINMENT_SECTION_START = '<EntertainmentSection>'
L_ENTERTAINMENT_SECTION_END = '</EntertainmentSection>'

L_SAMSUNG_SECTION_START = '<SamsungSection>'
L_SAMSUNG_SECTION_END = '</SamsungSection>'
L_SAMSUNG_DEVICE_END = '</Device>'

TESTING_SAMSUNG_DEVICE_NAME_0 = 'L/R TV 48abc1234'
TESTING_SAMSUNG_DEVICE_KEY_0 = '0'
TESTING_SAMSUNG_DEVICE_ACTIVE_0 = 'True'
TESTING_SAMSUNG_DEVICE_UUID_0 = 'Samsung.-0000-0000-0000-0123456789ab'
TESTING_SAMSUNG_DEVICE_COMMENT_0 = '46in 3D  '
TESTING_SAMSUNG_DEVICE_IPV4_0 = '192.168.1.118'
TESTING_SAMSUNG_DEVICE_PORT_0 = '55000'
TESTING_SAMSUNG_DEVICE_ROOM_NAME_0 = 'Living Room'
TESTING_SAMSUNG_DEVICE_ROOM_UUID_0 = 'Room....-0000-0000-0000-0123456789ab'
TESTING_SAMSUNG_DEVICE_TYPE_0 = 'TV'

L_SAMSUNG_DEVICE_START_0 = '    ' + \
    '<Device Name="' + TESTING_SAMSUNG_DEVICE_NAME_0 + \
    '" Key="' + TESTING_SAMSUNG_DEVICE_KEY_0 + \
    '" Active="' + TESTING_SAMSUNG_DEVICE_ACTIVE_0 + \
    '">'
L_SAMSUNG_UUID_0 = '<UUID>' + TESTING_SAMSUNG_DEVICE_UUID_0 + '</UUID>'
L_SAMSUNG_COMMENT_0 = '<Comment>' + TESTING_SAMSUNG_DEVICE_COMMENT_0 + '</Comment>'
L_SAMSUNG_IPV4_0 = '<IPv4>' + TESTING_SAMSUNG_DEVICE_IPV4_0 + '</IPv4>'
L_SAMSUNG_PORT_0 = '<Port>' + TESTING_SAMSUNG_DEVICE_PORT_0 + '</Port>'
L_SAMSUNG_ROOM_NAME_0 = '<RoomName>' + TESTING_SAMSUNG_DEVICE_ROOM_NAME_0 + '</RoomName>'
L_SAMSUNG_ROOM_UUID_0 = '<RoomUUID>' + TESTING_SAMSUNG_DEVICE_ROOM_UUID_0 + '</RoomUUID>'
L_SAMSUNG_TYPE_0 = '<Type>' + TESTING_SAMSUNG_DEVICE_TYPE_0 + '</Type>'

L_SAMSUNG_DEVICE_0 = '\n'.join([
    L_SAMSUNG_DEVICE_START_0,
    L_SAMSUNG_UUID_0,
    L_SAMSUNG_IPV4_0,
    L_SAMSUNG_PORT_0,
    L_SAMSUNG_DEVICE_END
])

XML_SAMSUNG_SECTION = '\n'.join([
    L_SAMSUNG_SECTION_START,
    L_SAMSUNG_DEVICE_0,
    L_SAMSUNG_SECTION_END
])

XML_ENTERTAINMENT = '\n'.join([
    L_ENTERTAINMENT_SECTION_START,
    XML_SAMSUNG_SECTION,
    L_ENTERTAINMENT_SECTION_END
])


ENTERTAINMENT_XSD = """
"""

# ## END DBK
