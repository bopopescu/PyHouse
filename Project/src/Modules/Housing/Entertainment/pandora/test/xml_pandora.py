"""
@name:      PyHouse/src/Modules/Housing/Entertainment/pandora/test/xml_pandora.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@note:      Created on Aug 03, 2018
@license:   MIT License
@summary:

<PandoraSection Active="True">
    <Type>Service</Type>
    <MaxSessions>1<MaxSessions>
    <Device Active="True" Key="0" Name="Running on pi-06-ct ">
        <Comment>Living Room</Comment>
        <Host>192.168.9.16</Host>
        <Type>Service</Type>
        <ConnectionFamily>Pioneer</ConnectionFamily>
        <ConnectionName>822-k</ConnectionName>
        <InputName>CD</InputName>
        <InputCode>01FN</InputCode>
        <Volume>47</Volume>
    </Device>
</PandoraSection>

"""

__updated__ = '2019-04-24'

TESTING_PANDORA_SECTION = 'PandoraSection'
TESTING_PANDORA_SERVICE = 'Service'

TESTING_PANDORA_ACTIVE = 'True'
TESTING_PANDORA_TYPE = 'Service'
TESTING_PANDORA_MAX_SESSIONS = '1'

L_PANDORA_SECTION_START = '<' + TESTING_PANDORA_SECTION + ' Active="' + TESTING_PANDORA_ACTIVE + '">'
L_PANDORA_SECTION_END = '</' + TESTING_PANDORA_SECTION + '>'
L_PANDORA_SERVICE_END = '</' + TESTING_PANDORA_SERVICE + '>'
L_PANDORA_SECTION_TYPE = '<Type>' + TESTING_PANDORA_TYPE + '</Type>'
L_PANDORA_MAX_SESSIONS = '<MaxSessions>' + TESTING_PANDORA_MAX_SESSIONS + '</MaxSessions>'

TESTING_PANDORA_SERVICE_NAME_0 = 'Running on pi-06-ct'
TESTING_PANDORA_SERVICE_KEY_0 = '0'
TESTING_PANDORA_SERVICE_ACTIVE_0 = 'True'
TESTING_PANDORA_SERVICE_COMMENT_0 = 'Living Room'
TESTING_PANDORA_SERVICE_HOST_0 = '192.168.9.16'
TESTING_PANDORA_SERVICE_MAX_PLAY_TIME_0 = '12345'
TESTING_PANDORA_SERVICE_TYPE_0 = 'Service'
TESTING_PANDORA_CONNECTION_DEVICE_FAMILY_0_0 = 'pioneer'
TESTING_PANDORA_CONNECTION_DEVICE_NAME_0_0 = '822-k'
TESTING_PANDORA_CONNECTION_INPUT_NAME_0_0 = 'CD'
TESTING_PANDORA_CONNECTION_INPUT_CODE_0_0 = '01FN'
TESTING_PANDORA_CONNECTION_DEFAULT_VOLUME_0_0 = '47'

L_PANDORA_SERVICE_START_0 = \
    '<' + TESTING_PANDORA_SERVICE + \
    ' Name="' + TESTING_PANDORA_SERVICE_NAME_0 + \
    '" Key="' + TESTING_PANDORA_SERVICE_KEY_0 + \
    '" Active="' + TESTING_PANDORA_SERVICE_ACTIVE_0 + \
    '">'
L_PANDORA_COMMENT_0 = '<Comment>' + TESTING_PANDORA_SERVICE_COMMENT_0 + '</Comment>'
L_PANDORA_HOST_0 = '<Host>' + TESTING_PANDORA_SERVICE_HOST_0 + '</Host>'
L_PANDORA_TYPE_0 = '<Type>' + TESTING_PANDORA_SERVICE_TYPE_0 + '</Type>'
L_PANDORA_CONNECTION_DEVICE_FAMILY_0 = '<ConnectionFamily>' + TESTING_PANDORA_CONNECTION_DEVICE_FAMILY_0_0 + '</ConnectionFamily>'
L_PANDORA_CONNECTION_DEVICE_NAME_0 = '<ConnectionName>' + TESTING_PANDORA_CONNECTION_DEVICE_NAME_0_0 + '</ConnectionName>'
L_PANDORA_DEVICE_MAX_PLAY_TIME_0 = '<MaxPlayTime>' + TESTING_PANDORA_SERVICE_MAX_PLAY_TIME_0 + '</MaxPlayTime>'
L_PANDORA_CONNECTION_INPUT_NAME_0 = '<InputName>' + TESTING_PANDORA_CONNECTION_INPUT_NAME_0_0 + '</InputName>'
L_PANDORA_CONNECTION_INPUT_CODE_0 = '<InputCode>' + TESTING_PANDORA_CONNECTION_INPUT_CODE_0_0 + '</InputCode>'
L_PANDORA_CONNECTION_DEFAULT_VOLUME_0 = '<Volume>' + TESTING_PANDORA_CONNECTION_DEFAULT_VOLUME_0_0 + '</Volume>'

L_PANDORA_SERVICE_0 = '\n'.join([
    L_PANDORA_SERVICE_START_0,
    L_PANDORA_COMMENT_0,
    L_PANDORA_HOST_0,
    L_PANDORA_DEVICE_MAX_PLAY_TIME_0,
    L_PANDORA_TYPE_0,
    L_PANDORA_CONNECTION_DEVICE_FAMILY_0,
    L_PANDORA_CONNECTION_DEVICE_NAME_0,
    L_PANDORA_CONNECTION_INPUT_NAME_0,
    L_PANDORA_CONNECTION_INPUT_CODE_0,
    L_PANDORA_CONNECTION_DEFAULT_VOLUME_0,
    L_PANDORA_SERVICE_END
])

XML_PANDORA_SECTION = '\n'.join([
    L_PANDORA_SECTION_START,
    L_PANDORA_SECTION_TYPE,
    L_PANDORA_MAX_SESSIONS,
    L_PANDORA_SERVICE_0,
    L_PANDORA_SECTION_END
])

# ## END DBK
