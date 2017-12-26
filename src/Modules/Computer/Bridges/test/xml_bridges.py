"""
@name:      PyHouse/src/Modules/Computer/Bridges/test/xml_bridges.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@note:      Created on Dec 22, 2017
@license:   MIT License
@summary:

BridgesSection
   Bridge (Name, Key, Active)
      UUID
      Comment
      IPv4Address
      Port
      Username
      Password

"""

__updated__ = '2017-12-26'

TESTING_BRIDGES_SECTION = 'BridgesSection'
TESTING_BRIDGE = 'Bridge'

L_BRIDGES_SECTION_START = '<' + TESTING_BRIDGES_SECTION + '>'
L_BRIDGES_SECTION_END = '</' + TESTING_BRIDGES_SECTION + '>'
L_BRIDGE_END = '    </' + TESTING_BRIDGE + '>'

TESTING_BRIDGE_NAME_0 = 'Insteon Hub'
TESTING_BRIDGE_KEY_0 = '0'
TESTING_BRIDGE_ACTIVE_0 = 'True'
TESTING_BRIDGE_UUID_0 = 'Bridge..-0001-0000-0000-0123456789ab'
TESTING_BRIDGE_COMMENT_0 = 'Insteon Hub'
TESTING_BRIDGE_CONNECTION_0 = 'Ethernet'
TESTING_BRIDGE_TYPE_0 = 'Insteon'
TESTING_BRIDGE_IPV4ADDRESS_0 = '192.168.1.134'
TESTING_BRIDGE_PORT_0 = '29105'
TESTING_BRIDGE_USERNAME_0 = 'Username'
TESTING_BRIDGE_PASSWORD_0 = 'Passwd'

L_BRIDGE_START_0 = '    ' + \
    '<' + TESTING_BRIDGE + ' ' + \
    'Name="' + TESTING_BRIDGE_NAME_0 + '" ' + \
    'Key="' + TESTING_BRIDGE_KEY_0 + '" ' + \
    'Active="' + TESTING_BRIDGE_ACTIVE_0 + '"' + \
    '>'
L_BRIDGE_UUID_0 = '      <UUID>' + TESTING_BRIDGE_UUID_0 + '</UUID>'
L_BRIDGE_COMMENT_0 = '      <Comment>' + TESTING_BRIDGE_COMMENT_0 + '</Comment>'
L_BRIDGE_IPV4_ADDRESS_0 = '      <IPv4Address>' + TESTING_BRIDGE_IPV4ADDRESS_0 + '</IPv4Address>'
L_BRIDGE_PORT_0 = '      <Port>' + TESTING_BRIDGE_PORT_0 + '</Port>'
L_BRIDGE_USERNAME_0 = '      <UserName>' + TESTING_BRIDGE_USERNAME_0 + '</UserName>'
L_BRIDGE_PASSWORD_0 = '      <Password>' + TESTING_BRIDGE_PASSWORD_0 + '</Password>'

L_BRIDGE_0 = '\n'.join([
    L_BRIDGE_START_0,
    L_BRIDGE_UUID_0,
    L_BRIDGE_COMMENT_0,
    L_BRIDGE_IPV4_ADDRESS_0,
    L_BRIDGE_PORT_0,
    L_BRIDGE_USERNAME_0,
    L_BRIDGE_PASSWORD_0,
    L_BRIDGE_END
])

TESTING_BRIDGE_NAME_1 = 'Philips Hue Hub'
TESTING_BRIDGE_KEY_1 = '1'
TESTING_BRIDGE_ACTIVE_1 = 'True'
TESTING_BRIDGE_UUID_1 = 'Bridge..-0002-0000-0000-0123456789ab'
TESTING_BRIDGE_COMMENT_1 = 'Hue Hub'
TESTING_BRIDGE_CONNECTION_1 = 'Ethernet'
TESTING_BRIDGE_TYPE_1 = 'Hue'
TESTING_BRIDGE_IPV4ADDRESS_1 = '192.168.1.111'
TESTING_BRIDGE_PORT_1 = '12345'
TESTING_BRIDGE_USERNAME_1 = 'Username-01'
TESTING_BRIDGE_PASSWORD_1 = 'Password-01'

L_BRIDGE_START_1 = '    ' + \
    '<' + TESTING_BRIDGE + ' ' + \
    'Name="' + TESTING_BRIDGE_NAME_1 + '" ' + \
    'Key="' + TESTING_BRIDGE_KEY_1 + '" ' + \
    'Active="' + TESTING_BRIDGE_ACTIVE_1 + '"' + \
    '>'
L_BRIDGE_UUID_1 = '      <UUID>' + TESTING_BRIDGE_UUID_1 + '</UUID>'
L_BRIDGE_COMMENT_1 = '      <Comment>' + TESTING_BRIDGE_COMMENT_1 + '</Comment>'
L_BRIDGE_IPV4_ADDRESS_1 = '      <IPv4Address>' + TESTING_BRIDGE_IPV4ADDRESS_1 + '</IPv4Address>'
L_BRIDGE_PORT_1 = '      <Port>' + TESTING_BRIDGE_PORT_1 + '</Port>'
L_BRIDGE_USERNAME_1 = '      <UserName>' + TESTING_BRIDGE_USERNAME_1 + '</UserName>'
L_BRIDGE_PASSWORD_1 = '      <Password>' + TESTING_BRIDGE_PASSWORD_1 + '</Password>'

L_BRIDGE_1 = '\n'.join([
    L_BRIDGE_START_1,
    L_BRIDGE_UUID_1,
    L_BRIDGE_COMMENT_1,
    L_BRIDGE_IPV4_ADDRESS_1,
    L_BRIDGE_PORT_1,
    L_BRIDGE_USERNAME_1,
    L_BRIDGE_PASSWORD_1,
    L_BRIDGE_END
])

XML_BRIDGES = '\n'.join([
    L_BRIDGES_SECTION_START,
    L_BRIDGE_0,
    L_BRIDGE_1,
    L_BRIDGES_SECTION_END
])

# ## END DBK
