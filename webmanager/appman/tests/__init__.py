import os

from django.conf import settings
from datetime import datetime, time
from django.core import mail
from django.core.files import File
from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import pre_save, post_save, post_delete


from appman.models import *
from appman.signals import *
from appman.utils.uncompress import UncompressThread
from appman.utils.fileutils import *
from appman.tests.settings import TestSettingsManager

def relative(*x):
    return os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), *x))

class ApplicationManagementTest(TestCase):
    
    def __init__(self, *args, **kwargs):
        super(ApplicationManagementTest, self).__init__(*args, **kwargs)
        self.settings_manager = TestSettingsManager()
        
        # Turn off signals
        pre_save.receivers = []
        post_save.receivers = []
        post_delete.receivers = []
    
    def setUp(self):
        self.extracted_folder = relative('../../tests/unzipped')
        if not os.path.exists(self.extracted_folder):
            os.mkdir(self.extracted_folder)
        self.settings_manager.set(WALL_APP_DIR=self.extracted_folder)
        
        
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
        response = self.client.get('/applications/')
        self.assertEqual(response.status_code, 302)
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
        
    def test_upload_app(self):
        """ Tests the Upload of a Zip file through the SWFUpload method. """
        login = self.do_login()
        
        zf = open(relative('../../tests/python_test_app.zip'),'rb')
        response = self.client.post('/applications/upload/', {
            'test': zf 
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ".zip")
        name = response.content.strip()
        zf.close()
        
        pf = open(relative('../../tests/wmlogo.png'),'rb')
        post_data = {
            'name': 'Yet another App',
            'zipfile': '',
            'hidFileID': name,
            'icon': pf,
            'category': self.educational.id, 
            'description': "Example app"
        }
        c = Application.objects.count()
        response = self.client.post('/applications/add/', post_data)
        self.assertEqual(c+1, Application.objects.count())
        self.assertRedirects(response, '/applications/%s/' % Application.objects.get(name='Yet another App').id)
        os.remove(relative('../../media/applications', name))
    
    def test_get_unique_path(self):
    	
    	new_file = 'test132.txt'
    	
    	# Test if it still doesn't exist
    	unique_file = get_unique_path(new_file)
    	self.assertEqual(unique_file, 'test132.txt')
    	
    	# Create it
    	new_file_path = relative(fullpath(new_file))
    	open(new_file_path,'a').close()
    	
    	# Get a unique path, now that the file already exists
    	unique_file = get_unique_path(new_file)
    	# Assert if the proper unique file path was given
    	self.assertEqual(unique_file, 'test132_.txt')
    	
    	os.remove(new_file_path)
        
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
        c = Application.objects.count()
        login = self.do_admin_login()
        response = self.client.get('/applications/%s/remove/' % self.gps.id)
        self.assertRedirects(response, '/applications/')
        self.assertEqual(c-1, Application.objects.count())

    def test_authorized_add_category(self):
        c = Category.objects.count()
        login = self.do_admin_login()
        post_data = {
            'name': 'Action'
        }
        response = self.client.post('/categories/add/', post_data)
        self.assertRedirects(response, '/categories/')
        self.assertEqual(c+1, Category.objects.count())
        
    def test_unauthorized_add_category(self):
        c = Category.objects.count()
        login = self.do_login()
        post_data = {
            'name': 'Action'
        }
        response = self.client.post('/categories/add/', post_data)
        self.assertRedirects(response, '/accounts/login/?next=/categories/add/')
        self.assertEqual(c, Category.objects.count())

    def test_authorized_list_cat(self):
        login = self.do_admin_login()
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Games</td>")
        self.assertContains(response, "<tr>", Category.objects.count()+1) # 2 cat, plus header
            
    def test_edit_cat(self):
        login = self.do_admin_login()
        #change educational to Work
        post_data = {
            'name': 'Work'
        }
        response = self.client.post('/categories/%s/edit/'%self.gps.category.id, post_data)
        #see if it changed
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Work</td>")
        self.assertContains(response, "<tr>", Category.objects.count()+1) # 2 cat, plus header
        #confirm that the application category changed to work
        response = self.client.get('/applications/%s/' % self.gps.id )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Work")

    def test_remove_unused_cat(self):
        login = self.do_admin_login()
        c = Category.objects.count()
        response = self.client.post('/categories/%s/remove/'%self.games.id)
        self.assertRedirects(response, '/categories/')
        self.assertEqual(c-1, Category.objects.count())

    def test_remove_used_cat(self):
        login = self.do_admin_login()
        c = Category.objects.count()
        response = self.client.post('/categories/%s/remove/'%self.gps.category.id)
        self.assertRedirects(response, '/categories/')
        #confirm that category unknow appeared
        response = self.client.get('/categories/')
        self.assertContains(response, DEFAULT_CATEGORY)        
        
        #confirm that the application category changed
        response = self.client.get('/applications/%s/'%self.gps.id)
        self.assertContains(response, DEFAULT_CATEGORY)                
    
    def test_default_category(self):
        self.assertEqual(Category.objects.filter(name=DEFAULT_CATEGORY).count(), 1)
        
    def test_register_with_different_passwords(self):
        u = User.objects.count()
        #try to register a user with different passwords
        post_data = {
            'username': 'test',
            'email': 'admin@student.dei.uc.pt',
            'password1': 'admin',
            'password2': 'administrator'
        }
        response = self.client.post('/accounts/register/', post_data)
    	#check the error message
    	self.assertContains(response, "Passwords do not match.")

    	#confirm that there is no new user.
    	self.assertEqual(User.objects.count(), u)
    
    def test_register_with_wrong_email(self):
        u = User.objects.count()
        #try to register a user with different passwords
        post_data = {
            'username': 'test',
            'email': 'admin@admin.pt',
            'password1': 'admin',
            'password2': 'admin'
        }
        response = self.client.post('/accounts/register/', post_data)
    	#check the error message
    	self.assertContains(response, "Email must be on uc.pt domain.")

        #confirm that there is no new user
    	self.assertEqual(User.objects.count(), u)
	
    def test_register_without_password(self):
        u = User.objects.count()
        #try to register a user with different passwords
        post_data = {
            'username': 'test',
            'email': 'admin@student.dei.uc.pt',
            'password1': '',
            'password2': ''
        }
        response = self.client.post('/accounts/register/', post_data)
    	#confirm that there is no new user
    	self.assertEqual(User.objects.count(), u)
	
	
    def test_register_sucessfull(self):
        u = User.objects.count()
        #try to register a user with different passwords
        post_data = {
            'username': 'test',
            'email': 'test@student.dei.uc.pt',
            'password1': 'testes',
            'password2': 'testes'
        }
        response = self.client.post('/accounts/register/', post_data)
    	#check the error message
    	self.assertRedirects(response, '/accounts/login/')

    	#confirm that there exists a new user
    	self.assertEqual(User.objects.count(), u+1)
	
    	#confirm that the email has been sent
    	self.assertEquals(len(mail.outbox),1)
        expected_subject = '[WallManager] Registration Complete'
        self.assertEquals(mail.outbox[0].subject, expected_subject)
        expected_from = 'wallmanager@dei.uc.pt'
        self.assertEquals(mail.outbox[0].from_email, expected_from)
        expected_to = 'test@student.dei.uc.pt'
        self.assertEquals(len(mail.outbox[0].to), 1)
        self.assertEquals(mail.outbox[0].to[0], expected_to)
        username = 'test'
    	expected_body = 'Dear ' + username + ', \nYour registration has been sucessfully complete.\n Best regards'
        self.assertEquals(mail.outbox[0].body, expected_body)	

    def tearDown(self):
        import shutil
        for app in Application.objects.all():
            if app.zipfile:
                app.zipfile.delete()
            if app.icon:
                app.icon.delete()
        shutil.rmtree(self.extracted_folder)
        self.settings_manager.revert()
        
