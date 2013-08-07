#! /usr/bin/env python
#-*- coding: iso-8859-1 -*-
"""
Created on Aug 3, 2013

@author: briank

Copyright (c) 2013 by D. Brian Kimmel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

This will take the distribution directory and move the needed files to the
correct place for running.

This may be run at any time to put new versions of the files to be moved.

Runs on:
    Windows 7
    Linux (OpenSuse 12.3)
    Raspberry Pi w/ Wheezy

"""

import sys

tests_passed = False


def FindOsRunning():
    """
    """
    import platform
    l_platform = platform.platform(True, True)
    print "Running on platform", l_platform


class TestInstalledSoftware(object):
    """Test to see if all required software is installed.
    """

    def test_python_version(self):
        l_version = sys.version_info
        if l_version.major != 2:
            print "ERROR - Only Python 2.7 is currently supported due to Twisted requirements."
            return False
        if l_version.minor < 7:
            print "ERROR - Python less than version is not tested - Please use 2.7.x"
            return False
        print "  Python 2.7 ok..."
        return True

    def test_twisted(self):
        try:
            import twisted
        except ImportError:
            print "ERROR - Twisted not installed.  apt-get install python-twisted"
            return False
        l_version = twisted.version
        if l_version.major < 12:
            print "ERROR - Twisted must be at least version 12.  apt-get install python-twisted"
        print "  Twisted > 12.0 ok..."
        return True

    def test_zope_interface(self):
        try:
            import zope.interface
        except ImportError:
            print "ERROR - Zope.Interface not installed.  apt-get install zope-interface"
            return False
        print "  Zope.interface ok..."
        return True

    def test_nevow(self):
        try:
            import nevow
        except ImportError:
            print "ERROR - Nevow not installed.  apt-get install nevow"
            return False
        print "  Nevow ok..."
        return True


class TestAll(object):
    """Test everything.
    """

    def __init__(self):
        global tests_passed
        print "Testing..."
        l_inst = TestInstalledSoftware()
        l_ok = l_inst.test_python_version()
        if l_ok:
            l_ok = l_inst.test_twisted()
        if l_ok:
            l_ok = l_inst.test_zope_interface()
        if l_ok:
            l_ok = l_inst.test_nevow()
        if l_ok:
            tests_passed = True


class Install(object):
    """
    """

    def __init__(self):
        print "Installing..."


if __name__ == "__main__":
    FindOsRunning()
    TestAll()
    if tests_passed:
        Install()
    else:
        print "Correct the above faults and rerun."

# ## END DBK