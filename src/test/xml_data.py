"""
@name:      PyHouse/src/test/xml_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jan 20, 2010
@summary:   Handle all of the information for all houses.

XML to define the PyHouse.xml file

used for testing
"""

# Import system type stuff

# Import PyMh files
from Modules.Computer.test.xml_computer import XML_COMPUTER_DIVISION
from Modules.Housing.test.xml_housing import HOUSE_DIVISION_XML, HOUSE_DIVISION_XML_1_3


TESTING_VERSION = """
    xmlns:comp="http://PyHouse.Org/ComputerDiv"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://PyHouse.org schemas/PyHouse.xsd"
>
<!-- Updated by PyHouse 2015-07-19 11:22:33.996000 -->
"""


# Missing
XML_MISSING = ''



# No sections
XML_EMPTY = """
<PyHouse
    Version='1.3.2'
    xmlns:comp="http://PyHouse.Org/ComputerDiv"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://PyHouse.org schemas/PyHouse.xsd"
>
<!-- Updated by PyHouse 2001-12-23 12:23:34.0 -->
</PyHouse>
"""



XML_SHORT = """
<PyHouse
    Version='1.3.2'
    xmlns:comp="http://PyHouse.Org/ComputerDiv"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://PyHouse.org schemas/PyHouse.xsd"
>
<!-- Updated by PyHouse 2001-12-23 12:23:34.0 -->
    <Web>
    </Web>
    <Nodes>
        <Node Name='PiNode-1' Key='0' Active='True'>
            <UUID>ec955bcf-89c9-11e3-b583-082e5f8cdfd2</UUID>
        </Node>
    </Nodes>
    <Houses>
        <House Name='House_1' Key='0' Active='True'>
            <Controllers>
                <Controller Name='Serial_1' Key='0' Active='True'>
                    <InterfaceType>Serial</InterfaceType>
                    <BaudRate>19200</BaudRate>
                    <ByteSize>8</ByteSize>
                    <DsrDtr>False</DsrDtr>
                    <Parity>N</Parity>
                    <RtsCts>False</RtsCts>
                    <StopBits>1.0</StopBits>
                    <Timeout>0</Timeout>
                    <XonXoff>False</XonXoff>
                </Controller>
                <Controller Name='USB_1' Key='1' Active='True'>
                    <InterfaceType>USB</InterfaceType>
                    <Vendor>12345</Vendor>
                    <Product>9876</Product>
                </Controller>
            </Controllers>
        </House>
    </Houses>
</PyHouse>
"""



L_PYHOUSE_HEADER_XML = """
<PyHouse
    Version='1.4.0'
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://PyHouse.org schemas/PyHouse.xsd">"""

L_PYHOUSE_HEADER_XML_1_3 = """
<PyHouse

    Version='1.3.2'
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://PyHouse.org schemas/PyHouse.xsd">"""

# Everything as expected in a running system.
XML_LONG = '\n'.join([
    L_PYHOUSE_HEADER_XML,
    XML_COMPUTER_DIVISION,
    HOUSE_DIVISION_XML,
    "</PyHouse>"
])

XML_LONG_1_3 = '\n'.join([
    L_PYHOUSE_HEADER_XML_1_3,
    XML_COMPUTER_DIVISION,
    HOUSE_DIVISION_XML_1_3,
    "</PyHouse>"
])


XSD_HEADER = """
"""

XSD_LONG = XSD_HEADER

# ## END DBK