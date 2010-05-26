#!/usr/bin/env python
import sys
import os
import unittest

for folder in ['webmanager','mtmenu']:
    sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), folder))

from webmanager.manage import *
import webmanager

from mtmenu.tests import TestMultiTouch

if __name__ == '__main__':
    
    def sep(title):
        print 20*"+"
        print title
        print 20*"+"
        
    sep("Wall Application")
    
    
    unittest.main()
    
    sep("Web Application")
    execute_manager(webmanager.settings, argv=['','test','appman'])
    
    