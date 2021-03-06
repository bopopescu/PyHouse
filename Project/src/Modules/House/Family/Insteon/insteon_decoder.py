"""
@name:      Modules/House/Family/insteon/insteon_decoder.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2020 by D. Brian Kimmel
@note:      Created on Feb 18, 2010  Split into separate file Jul 9, 2014
@license:   MIT License
@summary:   This module decodes insteon PLM response messages

For each message passed to this module:
    Decode message and extract information from the message.
    Where possible, get the object that sent the response message and place the gathered data back in that object.
    return a status flag of True if everything was OK.
    return a status flag of False if an error occurred.


This entire section was empirically derived with a little help from the Insteon Developers Manual.

The manual describes the fields in the message and not much more.

PLEASE REFACTOR ME!

"""

__updated__ = '2020-02-19'
__version_info__ = (19, 9, 22)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files
from Modules.House.Family.Insteon import insteon_utils
from Modules.House.Family.Insteon.insteon_hvac import DecodeResponses as DecodeHvac
from Modules.House.Family.Insteon.insteon_lighting import DecodeResponses as DecodeLighting
from Modules.House.Family.Insteon.insteon_security import DecodeResponses as DecodeSecurity
from Modules.House.Family.Insteon.insteon_link import DecodeLink as linkDecode
from Modules.House.Family.Insteon.insteon_constants import ACK, STX, X10_HOUSE, X10_UNIT, X10_COMMAND
from Modules.House.Family.Insteon.insteon_utils import Decode as utilDecode
from Modules.Core.Utilities.debug_tools import FormatBytes
from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.insteon_decode ')

#  OBJ_LIST = [Lights, Controllers, Buttons, Thermostats, Irrigation, Pool]


class DecodeResponses:

    m_pyhouse_obj = None
    m_controller_obj = None
    m_link = None

    def __init__(self, p_pyhouse_obj, p_controller_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj
        self.m_link = linkDecode(p_pyhouse_obj, p_controller_obj)
        LOG.info('Starting Decode')

    def decode_message(self, p_controller_obj):
        """Decode a message that was ACKed / NAked.
        see Insteon Developers Manual pages 238-241

        A controller response may contain multiple messages and the last message may not be complete.
        This should be invoked every time we pick up more messages from the controller.
        It should loop and decode each message present and leave when done

        @return: a flag that is True for ACK and False for NAK/Invalid response.
        """
        while len(p_controller_obj._Message) >= 2:
            l_stx = p_controller_obj._Message[0]
            if l_stx == STX:
                l_need_len = insteon_utils.get_message_length(p_controller_obj._Message)
                l_cur_len = len(p_controller_obj._Message)
                if l_cur_len >= l_need_len:
                    # LOG.debug('Got response:{}'.format(FormatBytes(p_controller_obj._Message[0:l_need_len])))
                    self._decode_dispatch(p_controller_obj)
                    return 'Ok'
                else:
                    LOG.debug('Message {:#02X} Needs {} bytes'.format(p_controller_obj._Message[1], l_need_len))
                    LOG.debug('Message was too short - waiting for rest of message. {}'.format(FormatBytes(p_controller_obj._Message)))
                    return 'Short'
            else:
                # LOG.warning("Dropping a leading char {:#x}  {}".format(l_stx, FormatBytes(p_controller_obj._Message)))
                p_controller_obj._Message = p_controller_obj._Message[1:]
                return 'Drop'

    def check_for_more_decoding(self, p_controller_obj, p_ret=True):
        """ Chop off the current message from the head of the buffered response stream from the controller.
        @param p_ret: is the result to return.
        """
        l_ret = p_ret
        l_cur_len = len(p_controller_obj._Message)
        l_chop = insteon_utils.get_message_length(p_controller_obj._Message)
        if l_cur_len >= l_chop:
            p_controller_obj._Message = p_controller_obj._Message[l_chop:]
            l_ret = self.decode_message(p_controller_obj)
        else:
            l_msg = "check_for_more_decoding() trying to chop an incomplete message - {}".format(
                    FormatBytes(p_controller_obj._Message))
            LOG.error(l_msg)
        return l_ret

    def _decode_dispatch(self, p_controller_obj):
        """ Decode a message that was ACKed / NAked.
        see IDM pages 238-241

        @return: a flag that is True for ACK and False for NAK/Invalid response.
        """
        l_message = p_controller_obj._Message
        l_cmd = p_controller_obj._Message[1]
        if l_cmd == 0:
            LOG.warning("Found a '0' record ->{}.".format(FormatBytes(l_message)))
            p_controller_obj._Message = p_controller_obj._Message[1:]
            return
        elif l_cmd == 0x50: self._decode_0x50(p_controller_obj)
        elif l_cmd == 0x51: self._decode_0x51(p_controller_obj)
        elif l_cmd == 0x52: self._decode_0x52_record(p_controller_obj)
        elif l_cmd == 0x53: self.m_link.decode_0x53(p_controller_obj)
        elif l_cmd == 0x54: self.m_link.decode_0x54(p_controller_obj)
        elif l_cmd == 0x55: self.m_link.decode_0x55(p_controller_obj)
        elif l_cmd == 0x56: self.m_link.decode_0x56(p_controller_obj)
        elif l_cmd == 0x57: self.m_link.decode_0x57(p_controller_obj)
        elif l_cmd == 0x58: self.m_link.decode_0x58(p_controller_obj)
        elif l_cmd == 0x60: self._decode_0x60_record(p_controller_obj)
        elif l_cmd == 0x61: self._decode_0x61_record(p_controller_obj)
        elif l_cmd == 0x62: self._decode_0x62_record(p_controller_obj)
        elif l_cmd == 0x64: self.m_link.decode_0x64(p_controller_obj)
        elif l_cmd == 0x65: self.m_link.decode_0x65(p_controller_obj)
        elif l_cmd == 0x69: self.m_link.decode_0x69(p_controller_obj)
        elif l_cmd == 0x6A: self.m_link.decode_0x6A(p_controller_obj)
        elif l_cmd == 0x6B: self._decode_0x6B_record(p_controller_obj)
        elif l_cmd == 0x6C: self.m_link.decode_0x6C(p_controller_obj)
        elif l_cmd == 0x6F: self.m_link.decode_0x6F(p_controller_obj)
        elif l_cmd == 0x73: self._decode_0x73_record(p_controller_obj)
        else:
            LOG.error("Unknown Insteon message {}, Cmd:{}".format(FormatBytes(p_controller_obj._Message), l_cmd))
        self.check_for_more_decoding(p_controller_obj)

    def XXX_publish(self, p_pyhouse_obj, p_device_obj):
        l_topic = "house/lighting/lights/{}/info".format(p_device_obj.Name)
        p_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, p_device_obj)  #  /lighting/{}/info

    def _decode_0x50(self, p_controller_obj):
        """ Insteon Standard Message Received (11 bytes)
        A Standard-length INSTEON message is received from either a Controller or Responder that you are ALL-Linked to.
        See p 233(246) of 2009 developers guide.
        [0] = x02
        [1] = 0x50
        [2-4] = from address
        [5-7] = to address / group
        [8] = message flags
        [9] = command 1
        [10] = command 2


        """
        l_message = p_controller_obj._Message
        l_device_obj = utilDecode().get_obj_from_message(self.m_pyhouse_obj, l_message[2:5])
        #
        if l_device_obj.DeviceType == 'Lighting':  # Light Type
            DecodeLighting().decode_0x50(self.m_pyhouse_obj, p_controller_obj, l_device_obj)
            return
        elif l_device_obj.DeviceType == 'Hvac':  # HVAC Type
            DecodeHvac().decode_0x50(self.m_pyhouse_obj, p_controller_obj, l_device_obj)
            return
        elif l_device_obj.DeviceType == 'Security':  # Security Type
            DecodeSecurity().decode_0x50(self.m_pyhouse_obj, p_controller_obj, l_device_obj)
            return
        else:
            LOG.error('Unknown Device Type:{};'.format(l_device_obj.DeviceType))
            return

    def _decode_0x51(self, p_controller_obj):
        """ Insteon Extended Message Received (25 bytes).
        See p 234(247) of 2009 developers guide.
        """
        l_message = p_controller_obj._Message
        l_obj_from = utilDecode().get_obj_from_message(self.m_pyhouse_obj, l_message[2:5])
        _l_obj_to = utilDecode().get_obj_from_message(self.m_pyhouse_obj, l_message[5:8])
        _l_flags = l_message[8]
        l_cmd1 = l_message[9]
        l_cmd2 = l_message[10]
        l_extended = "{:X}.{:X}.{:X}.{:X}.{:X}.{:X}.{:X}.{:X}.{:X}.{:X}.{:X}.{:X}.{:X}.{:X}".format(
                    l_message[11], l_message[12], l_message[13], l_message[14], l_message[15], l_message[16], l_message[17],
                    l_message[18], l_message[19], l_message[20], l_message[21], l_message[22], l_message[23], l_message[24])
        if l_cmd1 == 0x03 and l_cmd2 == 0:  # Product Data request response
            l_product_key = self._get_addr_from_message(l_message, 12)
            l_devcat = l_message[15] * 256 + l_message[16]
            LOG.info('ProdData Fm:"{}"; ProductID:"{}"; Dev-Cat:"{}"; Data:"{}"'.format(l_obj_from.Name, l_product_key, l_devcat, l_extended))
            l_obj_from.ProductKey = l_product_key
            l_obj_from.DevCat = l_devcat
        p_controller_obj.Ret = True
        insteon_utils.update_insteon_obj(self.m_pyhouse_obj, l_obj_from)
        return

    def _decode_0x52_record(self, p_controller_obj):
        """Insteon X-10 message received (4 bytes).
        See p 240(253) of 2009 developers guide.
        [0] = x02
        [1] = 0x52
        [2] = high order 4 bits contain house code, low order 4 bits contain key code.
        [3] = flag 0x00 indicates key code is unit code; 0x80 indicates key code is command.

        0x0    M    13    All Units Off
        0x1    E     5    All Lights On
        0x2    C     3    On
        0x3    K    11    Off
        0x4    O    15    Dim
        0x5    G     7    Bright
        0x6    A     1    All Lights Off
        0x7    I     9    Extended Code
        0x8    N    14    Hail Request
        0x9    F     6    Hail Acknowledge
        0xA    D     4    Preset Dim
        0xB    L    12    Preset Dim
        0xC    P    16    Extended Data (analog)
        0xD    H     8    Status = On
        0xE    B     2    Status = Off
        0xF    J    10    Status Request
        """
        l_message = p_controller_obj._Message
        l_house = X10_HOUSE[(l_message[2] >> 4) & 0x0F]
        l_key = l_message[2] & 0x0F
        l_unit = ''
        l_command = ''
        if l_message[3] == 0:
            l_unit = X10_UNIT[l_key]
        else:
            l_command = X10_COMMAND[l_key]
        LOG.info("X10 Message - House:{} {}, Command:{}".format(l_house, l_unit, l_command))

    def _decode_0x60_record(self, p_controller_obj):
        """Get Insteon Modem Info (9 bytes).
        See p 273 of developers guide.
        """
        l_message = p_controller_obj._Message
        l_obj = utilDecode().get_obj_from_message(self.m_pyhouse_obj, l_message[2:5])
        l_devcat = l_message[5]
        l_devsubcat = l_message[6]
        l_firmver = l_message[7]
        LOG.info("== 60 - Insteon Modem Info - Dev-Cat={}, DevSubCat={}, Firmware={} - Name={}".format(l_devcat, l_devsubcat, l_firmver, l_obj.Name))
        if l_message[8] == ACK:
            insteon_utils.update_insteon_obj(self.m_pyhouse_obj, l_obj)
            p_controller_obj.Ret = True
        else:
            LOG.error("== 60 - No ACK - Got {:#x}".format(l_message[8]))
            p_controller_obj.Ret = False
        return

    def _decode_0x61_record(self, p_controller_obj):
        """ Get response to - Send All-Link command (6 bytes).
        See p 241(254) of 2009 developers guide.
        """
        l_message = p_controller_obj._Message
        l_grp = l_message[2]
        l_cmd1 = l_message[3]
        l_cmd2 = l_message[4]
        l_ack = l_message[5]
        LOG.info("All-Link Ack - Group:{}, Cmd:{}, Bcst:{}, Ack:{}".format(l_grp, l_cmd1, l_cmd2, l_ack))
        if l_ack == ACK:
            p_controller_obj.Ret = True
        else:
            LOG.error("== 61 - No ACK - Got {:#x}".format(l_ack))
            p_controller_obj.Ret = False
        return

    def _decode_0x62_record(self, p_controller_obj):
        """Get response to Send Insteon standard-length message (9 bytes).
        Basically, a response to the 62 command.
        See p 230(243) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x62
        [2-4] = address
        [5] = message flags
        [6] = command 1
        [7] = command 2
        [8] = ACK/NAK  (SD)

        [8] = User Data 1  (ED)
        [9] = User Data 2
        [10] = User Data 3
        [11] = User Data 4
        [12] = User Data 5
        [13] = User Data 6
        [14] = User Data 7
        [15] = User Data 8
        [16] = User Data 9
        [17] = User Data 10
        [18] = User Data 11
        [19] = User Data 12
        [20] = User Data 13
        [21] = User Data 14
        [22] = ACK/NAK
        This is an ack/nak of the command and generally is not very interesting by itself.
        Depending on the command sent, another response MAY follow this message with further data.
        """
        l_message = p_controller_obj._Message
        l_obj = utilDecode().get_obj_from_message(self.m_pyhouse_obj, l_message[2:5])
        _l_msgflags = utilDecode._decode_insteon_message_flag(l_message[5])
        l_ext = (l_message[5] & 0x10) >> 4
        if l_ext:
            l_message = l_message[:23]
            l_ack = utilDecode.get_ack_nak(l_message[22])
            l_debug_msg = FormatBytes(l_message)
            LOG.debug('Got response(0x62) {}'.format(l_debug_msg))
        else:
            l_message = l_message[:9]
            l_ack = utilDecode.get_ack_nak(l_message[8])
            l_debug_msg = "Device: {}, {}".format(l_obj.Name, l_ack)
        if l_ack != 'ACK ':
            LOG.debug('Got response(0x62) "{}"'.format(l_ack))
        return

    def _decode_0x67_record(self, p_controller_obj):
        """Reset IM ACK response (3 bytes).
        See p 258 of developers guide.
        """
        l_message = p_controller_obj._Message
        l_ack = utilDecode.get_ack_nak(l_message[2])
        l_debug_msg = "Reset IM(PLM) {}".format(l_ack)
        LOG.info("{}".format(l_debug_msg))
        return

    def _decode_0x6B_record(self, p_controller_obj):
        """Get set IM configuration (4 bytes).
        See p 258(271) of 2009 developers guide.
        [0] = x02
        [1] = 0x6B
        [2] = Flags
        [3] = ACK/NAK
         """
        l_message = p_controller_obj._Message
        l_flag = l_message[2]
        l_ack = utilDecode.get_ack_nak(l_message[3])
        l_debug_msg = "Config flag from PLM:{} - ConfigFlag:{:#02X}, {}".format(p_controller_obj.Name, l_flag, l_ack)
        LOG.info("Received from {}".format(l_debug_msg))
        if l_message[3] == ACK:
            p_controller_obj.Ret = True
        else:
            LOG.error("== 6B - NAK/Unknown message type {:#x}".format(l_flag))
            p_controller_obj.Ret = False
        return

    def _decode_0x73_record(self, p_controller_obj):
        """ Get the PLM response of 'get config' (6 bytes).
        See p 257(270) of the 2009 developers guide.
        [0] = x02
        [1] = IM Control Flag
        [2] = Spare 1
        [3] = Spare 2
        [4] = ACK/NAK
        """
        l_message = p_controller_obj._Message
        l_flags = l_message[2]
        l_spare1 = l_message[3]
        l_spare2 = l_message[4]
        l_ack = utilDecode.get_ack_nak(l_message[5])
        LOG.info("== 0x73 Get IM configuration Flags={:#x}, Spare 1={:#x}, Spare 2={:#x} {} ".format(
                    l_flags, l_spare1, l_spare2, l_ack))
        return

#  ## END DBK
