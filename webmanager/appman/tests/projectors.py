import cgi
import BaseHTTPServer
from SocketServer import ThreadingMixIn
from threading import Thread

from django.test import TestCase
from django.conf import settings

from appman.utils.projectors import *

global local_log
local_log = []

class FakeProjectorManager(ProjectorManager):
    def __init__(self, ip):
        self.ip = ip
    
    def login(self):
        local_log.append("login")
        return True

    def set_time(self, day, h, m, s):
        local_log.append("set_time %s %s %s" % (s,h,m) )
    
    def enable(self,day):
        local_log.append("enable")
    
    def reset(self,day):
        local_log.append("reset")

class ProjectorTest(TestCase):
    def setUp(self):
        global local_log
        local_log = []
    
    def test_projector_sequence(self):
        """ Tests the sequence of projectors """
        set_projectors_time((10,1), (10,2), (11,00), (12,00), 
                klass=FakeProjectorManager, projector_ips = [None])
        
        expected_log = (['login'] + 
                        5 * ['reset', 'set_time 1 10 1', 'set_time 0 10 2', 'enable'] +
                        2 * ['reset', 'set_time 1 11 0', 'set_time 0 12 0', 'enable'])
        
        self.assertEquals(local_log, expected_log)
    
    def tearUp(self):
        pass
