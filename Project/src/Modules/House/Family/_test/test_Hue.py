"""
-*- _test-case-name: /home/briank/workspace/PyHouse/src/Modules/Families/_test/test_Hue.py -*-

@name:      /home/briank/workspace/PyHouse/src/Modules/Families/_test/test_Hue.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@note:      Created on Dec 18, 2017
@license:   MIT License
@summary:

Passed all tests - DB - 2018-02-13

"""

__updated__ = '2018-02-13'

# Import system type stuff
from twisted.trial import unittest, reporter, runner

# Import PyMh files and modules.
from Modules.Families.Hue import test as I_test


class Z_Hue(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_Hue(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter()
        l_package.run(l_ret)
        l_ret.done()
        #
        print('\n====================\n*** test_Hue ***\n{}\n'.format(l_ret))

# ## END DBK