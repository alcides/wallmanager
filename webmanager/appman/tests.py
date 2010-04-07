from datetime import time
from django.test import TestCase
from appman.models import *

class ApplicationManagement(TestCase):
    
    def setUp(self):
        #Creates usernames for Zacarias and Mario Zenha-Rela
        self.zacarias = User.objects.create(email="zacarias@student.dei.uc.pt")
        self.mzr = User.objects.create(email="mzr@dei.uc.pt", level="A")
		
        self.educational = Category.objects.create(name="Educational")
        self.games = Category.objects.create(name="Games")
        
        self.gps = Application.objects.create(name="Gps Application", owner=self.mzr, category=self.educational)
    
    def test_models_representation(self):
        self.assertEqual( unicode(self.mzr), u"mzr@dei.uc.pt" )
        self.assertEqual( unicode(self.educational), u"Educational" )
        self.assertEqual( unicode(self.gps), u"Gps Application" )
    
    def test_application_value(self):
        self.gps.likes = 5
        self.gps.dislikes = 3
        self.gps.save()
        self.assertEqual( self.gps.value(), 2)
    
    def test_uniqueness_superadmin(self):
        su1 = User.objects.create(email="su1@dei.uc.pt", level='S')
        su2 = User.objects.create(email="su2@dei.uc.pt", level='S')
        
        self.assertEqual( User.objects.filter(level='S').count(), 1)
        self.assertEqual( User.objects.get(email="su1@dei.uc.pt").level, 'A')
        self.assertEqual( User.objects.get(email="su2@dei.uc.pt").level, 'S')
    
    def test_uniqueness_control(self):
        c1 = ProjectorControl.objects.create(inactivity_time=1, startup_time=time(1), shutdown_time=time(2))
        c2 = ProjectorControl.objects.create(inactivity_time=1, startup_time=time(1), shutdown_time=time(3))
        self.assertEqual( ProjectorControl.objects.count(), 1)
        
    def test_application_log(self):
        self.log = ApplicationLog.objects.create(application=self.gps, error_description="The application reported a certain exception, which is...")
        print self.log
    
    def tearDown(self):
        pass
        