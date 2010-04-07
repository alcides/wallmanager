from datetime import datetime, time
from django.test import TestCase
from appman.models import *

class ApplicationManagement(TestCase):
    
    def setUp(self):
        #Creates usernames for Zacarias and Prof. Plum
        self.zacarias = User.objects.create(email="zacarias@student.dei.uc.pt")
        self.plum = User.objects.create(email="plum@dei.uc.pt", level="A")
		
        self.educational = Category.objects.create(name="Educational")
        self.games = Category.objects.create(name="Games")
        
        self.gps = Application.objects.create(name="Gps Application", owner=self.plum, category=self.educational)
    
    def test_models_representation(self):
        self.assertEqual( unicode(self.plum), u"plum@dei.uc.pt" )
        self.assertEqual( unicode(self.educational), u"Educational" )
        self.assertEqual( unicode(self.gps), u"Gps Application" )
    
    def test_application_value(self):
        self.gps.likes = 5
        self.gps.dislikes = 3
        self.gps.save()
        self.assertEqual( self.gps.value(), 0.625)
        self.assertEqual( self.gps.stars(), 3)
    
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
        
    def test_application_log_representation(self):
        self.log = ApplicationLog.objects.create(application=self.gps, error_description="Error importing library X.")
        self.log.datetime = datetime(2010,1,1,15,0,1)
        self.log.save()
        self.assertEqual( unicode(self.log),  u"Gps Application log at 2010-01-01 15:00:01")
    
    def tearDown(self):
        pass
        