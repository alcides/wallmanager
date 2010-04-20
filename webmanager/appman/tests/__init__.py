from datetime import datetime, time
from django.core import mail
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files import File
from django.db.models.signals import pre_save, post_save, post_delete

from appman.models import *
from appman.signals import get_app_dir
from appman.utils.fileutils import relative
from appman.tests.uncompress import UncompressTest

class ApplicationManagementTest(TestCase):
    def __init__(self, *args, **kwargs):
        super(ApplicationManagementTest, self).__init__(*args, **kwargs)
        
        # Turn off signals
        pre_save.receivers = []
        post_save.receivers = []
        post_delete.receivers = []
    
    def setUp(self):
        #Creates usernames for Zacarias and Prof. Plum
        self.zacarias = User.objects.create_user(username="zacarias_stu", email="zacarias@student.dei.uc.pt", password="zacarias")
        self.plum = User.objects.create_user(username="plum_ede", email="plum@dei.uc.pt", password="plum")
        self.plum.is_staff = True
        self.plum.is_superuser = True
        self.plum.save()
        		
        self.educational = Category.objects.create(name="Educational")
        self.games = Category.objects.create(name="Games")
        
        self.gps = Application.objects.create(name="Gps Application", owner=self.zacarias, category=self.educational)
        
    def do_login(self):
        login = self.client.login(username='zacarias_stu', password='zacarias')
        self.assertEqual(login, True)
        return login

    def do_admin_login(self):
        login = self.client.login(username='plum_ede', password='plum')
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
        
    def test_application_log_representation(self):
        self.log = ApplicationLog.objects.create(application=self.gps, error_description="Error importing library X.")
        self.log.datetime = datetime(2010,1,1,15,0,1)
        self.log.save()
        self.assertEqual( unicode(self.log),  u"Gps Application log at 2010-01-01 15:00:01")

    def test_list_app(self):
        login = self.do_login()
        response = self.client.get('/applications/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gps Application</a></td>")
        self.assertContains(response, "<tr>", 2) # 1 app, plus header
        
    def test_detail_app(self):
        response = self.client.get('/applications/%s/' % self.gps.id )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gps Application")
        self.assertContains(response, "Edit Application",0)
        
        login = self.do_login()
        response = self.client.get('/applications/%s/' % self.gps.id )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Application",1)

    def test_requires_login_to_add_app(self):
        response = self.client.get('/applications/add/')
        self.assertEqual(response.status_code, 302) # redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/applications/add/')
    
    def test_add_app(self):
        login = self.do_login()
        response = self.client.get('/applications/add/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add Application")
        self.assertContains(response, "<form", 1)

        zf = open(relative('../../tests/python_test_app.zip'),'rb')
        pf = open(relative('../../tests/wmlogo.png'),'rb')
        post_data = {
            'name': 'Example App',
            'zipfile': zf,
            'icon': pf,
            'category': self.educational.id, 
            'description': "Example app"
        }
        response = self.client.post('/applications/add/', post_data)
        zf.close()
        pf.close()

        self.assertRedirects(response, '/applications/%s/' % Application.objects.get(name='Example App').id)
        response = self.client.get('/applications/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Example App</a></td>")
            
    def test_requires_login_to_edit_app(self):
        response = self.client.get('/applications/%s/edit/' % self.gps.id)
        self.assertEqual(response.status_code, 302) # redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/applications/%s/edit/' % self.gps.id)

    def test_edit_app(self):
        login = self.do_login()
        response = self.client.get('/applications/%s/edit/' % self.gps.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Application")
        
        zf = open(relative('../../tests/python_test_app.zip'),'rb')
        pf = open(relative('../../tests/wmlogo.png'),'rb')
        post_data = {
            'name': 'Example App 2',
            'zipfile': zf,
            'icon': pf,
            'category': self.educational.id, 
            'description': "Example app"
        }
        
        response = self.client.post('/applications/%s/edit/' % self.gps.id, post_data)
        zf.close()
        pf.close()
        
        self.assertRedirects(response, '/applications/%s/' % self.gps.id)
        response = self.client.get('/applications/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Example App 2</a></td>")

    def test_delete_app(self):
        c = Application.objects.count()
        login = self.do_login()
        response = self.client.get('/applications/%s/delete/' % self.gps.id)
        self.assertRedirects(response, '/applications/')
        self.assertEqual(c-1, Application.objects.count())

    def test_requires_staff_to_remove_app(self):
        c = Application.objects.count()
        login = self.do_login()
        response = self.client.get('/applications/%s/remove/' % self.gps.id)
        self.assertRedirects(response, '/accounts/login/?next=/applications/%s/remove/'% self.gps.id)
        self.assertEqual(c, Application.objects.count())
        
    def test_remove_app(self):
        # Clean email inbox
        mail.outbox = []
        
        c = Application.objects.count()
        login = self.do_admin_login()
        response = self.client.get('/applications/%s/remove/' % self.gps.id)
        self.assertRedirects(response, '/applications/')
        self.assertEqual(c-1, Application.objects.count())
        
        self.assertEquals(len(mail.outbox), 1)
        self.assertTrue("Application removed from the wall" in mail.outbox[0].subject)
        

    
    def tearDown(self):
        pass
        