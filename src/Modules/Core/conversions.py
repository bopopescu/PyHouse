"""
-*- test-case-name: PyHouse/src/Modules/Core/test/test_Insteon_utils.py -*-

@name: PyHouse/src/Modules/Core/conversions.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jul 14, 2014
@summary: This module is for conversion routines.

"""

# Import system type stuff
import math



"""
Internally, things are stored as integers but when working with humans dotted hex is easier to remember.

So for 1 to 4 bytes we convert 123456 to 'A1.b2.C3' and visa-versa.
"""
def _get_factor(p_size):
    """Internal utility to get a power of 256 (1 byte)
    """
    if p_size <= 1:
        return 0
    l_ix = int(math.pow(256, (p_size - 1)))
    return l_ix


def dotted_hex2int(p_hex):
    """
    @param p_hex: is a str like 'A1.B2.C3'
    """
    p_hex.replace(':', '.')
    l_hexn = ''.join(["%02X" % int(l_ix, 16) for l_ix in p_hex.split('.')])
    return int(l_hexn, 16)

def int2dotted_hex(p_int, p_size):
    """
    @param p_int: is the integer to convert to a dotted hex string such as 'A1.B2' or 'C4.D3.E2'
    @param p_size: is the number of bytes to convert - either 2 or 3
    """
    l_ix = _get_factor(p_size)
    l_hex = []
    while l_ix > 0:
        l_byte, p_int = divmod(p_int, l_ix)
        l_hex.append("{0:02X}".format(l_byte))
        l_ix = l_ix / 256
    return str('.'.join(l_hex))

# ## END DBK