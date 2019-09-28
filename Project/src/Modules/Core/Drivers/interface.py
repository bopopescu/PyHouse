"""
@name:      Modules/Core/Drivers/interface.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 21, 2013
@summary:

There is no need to pre-load any interfaces.
The necessary interfaces are discovered when loading the "devices" that are controlled by PyHouse.

Controllers, which are attached to the server, communicate with the server via an interface.
"""

__updated__ = '2019-09-25'
__version_info__ = (19, 9, 22)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff

# Import PyMh files
from Modules.Core.Config import config_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Drivers.Serial import Serial_driver

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Interface      ')


class DriverInterfaceInformation:
    """
    ...Interface.xxxx
    """

    def __init__(self):
        self.Type = None  # Null, Ethernet, Serial, USB, HTML, Websockets,  ...
        self.Host = None
        self.Port = None
        self._DriverApi = None  # Serial_driver.API()
        # Type specific information follows


def _get_interface_type(p_device_obj):
    return p_device_obj.Interface.Type.lower()


def get_device_driver_API(p_pyhouse_obj, p_interface_obj):
    """
    Based on the InterfaceType of the controller, load the appropriate driver and get its API().
    @return: a pointer to the device driver or None
    """
    # LOG.debug(PrettyFormatAny.form(p_interface_obj, 'DriverInterface'))
    l_type = p_interface_obj.Type.lower()
    if l_type == 'serial':
        # LOG.debug('Getting Serial Interface')
        l_driver = Serial_driver.API(p_pyhouse_obj)

    elif l_type == 'ethernet':
        from Modules.Core.Drivers.Ethernet import Ethernet_driver
        l_driver = Ethernet_driver.API(p_pyhouse_obj)

    elif l_type == 'usb':
        from Modules.Core.Drivers.USB import USB_driver
        l_driver = USB_driver.API(p_pyhouse_obj)

    else:
        LOG.error('No driver for device: {} with interface type: {}'.format(
                l_type, p_interface_obj.Type))
        from Modules.Core.Drivers.Null import Null_driver
        l_driver = Null_driver.API(p_pyhouse_obj)

    p_interface_obj._DriverApi = l_driver
    # l_driver.Start(p_controller_obj)
    return l_driver


class Config:
    """ This abstracts the interface information.
    Used so far for lighting controllers.
    Allows for yaml config files to have a section for "Interface:" without defining the contents of that section;
     getting that information is the job of the particular driver XXX

    Interface:
       Type: Serial
       Host: pi-01-pp
       Port: /dev/ttyUSB0
       <Type specific information>
       ...
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def extract_interface_group(self, p_config):
        """ Get the Interface sub-fields
        """
        LOG.debug('Getting interface')
        l_obj = DriverInterfaceInformation()
        l_required = ['Type', 'Host', 'Port']
        l_allowed = ['ApiKey', 'AccessKey']
        config_tools.Tools(self.m_pyhouse_obj).extract_fields(l_obj, p_config, l_required, l_allowed)
        #
        LOG.debug('Getting driver API')
        l_driver = get_device_driver_API(self.m_pyhouse_obj, l_obj)
        l_obj._DriverApi = l_driver
        LOG.debug(PrettyFormatAny.form(l_obj, 'Interface'))
        return l_obj

# ## END DBK