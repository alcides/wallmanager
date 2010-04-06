from datetime import time

from django.test import TestCase
from django.contrib.auth.models import User

from appman.models import *

class ApplicationManagement(TestCase):
    
    def setUp(self):
        #Creates usernames for Zacarias and Prof. Plum
        self.zacarias = User.objects.create(username="zacarias_stu", email="zacarias@student.dei.uc.pt")
        self.plum = User.objects.create(username="plum_ede", email="plum@dei.uc.pt", is_staff=True, is_superuser=True)
		
        self.educational = Category.objects.create(name="Educational")
        self.games = Category.objects.create(name="Games")
        
        self.gps = Application.objects.create(name="Gps Application", owner=self.plum, category=self.educational)
    
    def test_models_representation(self):
        self.assertEqual( unicode(self.educational), u"Educational" )
        self.assertEqual( unicode(self.gps), u"Gps Application" )
    
    def test_application_value(self):
        self.gps.likes = 5
        self.gps.dislikes = 3
        self.gps.save()
        self.assertEqual( self.gps.value(), 0.625)
        self.assertEqual( self.gps.stars(), 3)
    
    def test_uniqueness_control(self):
        c1 = ProjectorControl.objects.create(inactivity_time=1, startup_time=time(1), shutdown_time=time(2))
        c2 = ProjectorControl.objects.create(inactivity_time=1, startup_time=time(1), shutdown_time=time(3))
        self.assertEqual( ProjectorControl.objects.count(), 1)
        
    def test_list_app(self):
        response = self.client.get('/app/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<td>Gps Application</td>")
        self.assertContains(response, "<tr>", 2) # 1 app, plus header


    def tearDown(self):
        pass
        