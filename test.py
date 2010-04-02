#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "webmanager"))

from webmanager.manage import *
import webmanager

execute_manager(webmanager.settings, argv=['','test','appman'])