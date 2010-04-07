from datetime import time

from django.test import TestCase
from django.contrib.auth.models import User

from appman.models import *

import os
def relative(*x):
	return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

class ApplicationManagement(TestCase):
    
    def setUp(self):
        #Creates usernames for Zacarias and Prof. Plum
        self.zacarias = User.objects.create_user(username="zacarias_stu", email="zacarias@student.dei.uc.pt", password="zacarias")
        self.plum = User.objects.create_user(username="plum_ede", email="plum@dei.uc.pt", password="plum")
        self.plum.is_staff = True
        self.plum.is_superuser = True
        self.plum.save()
        		
        self.educational = Category.objects.create(name="Educational")
        self.games = Category.objects.create(name="Games")
        
        self.gps = Application.objects.create(name="Gps Application", owner=self.plum, category=self.educational)
 
    def do_login(self):
        login = self.client.login(username='zacarias_stu', password='zacarias')
        self.assertEqual(login, True)
        return login
   
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

    def test_requires_login_to_add_app(self):
        response = self.client.get('/app/add/')
        self.assertEqual(response.status_code, 302) # redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/app/add/')
    
    def test_add_app(self):
        login = self.do_login()
        response = self.client.get('/app/add/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form", 1)

        zf = open(relative('../tests/python_test_app.zip'))
        pf = open(relative('../tests/wmlogo.png'))
        post_data = {
            'name': 'Example App',
            'zipfile': zf,
            'icon': pf,
            'category': self.educational.id, 
            'description': "Example app"
        }
        response = self.client.post('/app/add/', post_data)
        zf.close()
        pf.close()
        
        self.assertRedirects(response, '/app/list/')
        response = self.client.get('/app/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<td>Example App</td>")

    def test_edit_app(self):
        login = self.do_login()
        response = self.client.get('/app/edit/%s' % self.gps.id)
        self.assertEqual(response.status_code, 200)
        
        zf = open(relative('../tests/python_test_app.zip'))
        pf = open(relative('../tests/wmlogo.png'))
        post_data = {
            'name': 'Example App 2',
            'zipfile': zf,
            'icon': pf,
            'category': self.educational.id, 
            'description': "Example app"
        }
        
        response = self.client.post('/app/edit/%s' % self.gps.id, post_data)
        zf.close()
        pf.close()
        
        self.assertRedirects(response, '/app/list/')
        response = self.client.get('/app/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<td>Example App 2</td>")

    def test_delete_app(self):
        c = Application.objects.count()
        login = self.do_login()
        response = self.client.get('/app/delete/%s' % self.gps.id)
        self.assertRedirects(response, '/app/list/')
        self.assertEqual(c-1, Application.objects.count())

    def tearDown(self):
        pass
        