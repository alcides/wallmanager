import os

from datetime import datetime, time
from django.core import mail
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.core.files import File
from django.db.models.signals import pre_save, post_save, post_delete

from appman.models import *
from appman.signals import get_app_dir, remove_extra_logs
from appman.utils.fileutils import *
from appman.utils import get_contact_admin_email
#from appman.tests.uncompress import UncompressTest

APPS_MAX_LOG_ENTRIES = 5
DEFAULT_CATEGORY = "Others"

class ApplicationManagementTest(TestCase):
    def __init__(self, *args, **kwargs):
        super(ApplicationManagementTest, self).__init__(*args, **kwargs)
        
        # Turn off signals except remove_logs
        post_save.receivers = []
        post_delete.receivers = []

        post_save.connect(remove_extra_logs, sender=ApplicationLog)
    
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
        """ Fakes login as standard user. """
        login = self.client.login(username='zacarias_stu', password='zacarias')
        self.assertEqual(login, True)
        return login

    def do_admin_login(self):
        """ Fakes login as administrator. """
        login = self.client.login(username='plum_ede', password='plum')
        self.assertEqual(login, True)
        return login
   
    def test_models_representation(self):
        """ Tests if categories are being well represented as strings. """
        self.assertEqual( unicode(self.educational), u"Educational" )
        self.assertEqual( unicode(self.gps), u"Gps Application" )
    
    def test_application_value(self):
        """ Tests application ratings. """
        self.gps.likes = 5
        self.gps.dislikes = 3
        self.gps.save()
        self.assertEqual( self.gps.value(), 0.625)
        self.assertEqual( self.gps.stars(), 3)
    
    def test_uniqueness_control(self):
        """ Tests uniqueness of the Projector Control object. """
        c1 = ProjectorControl.objects.create(inactivity_time=1, startup_time=time(1), shutdown_time=time(2))
        c2 = ProjectorControl.objects.create(inactivity_time=1, startup_time=time(1), shutdown_time=time(3))
        self.assertEqual( ProjectorControl.objects.count(), 1)
        
    def test_application_log_representation(self):
        """ Tests if logs are well represented. """
        self.log = ApplicationLog.objects.create(application=self.gps, error_description="Error importing library X.")
        self.log.datetime = datetime(2010,1,1,15,0,1)
        self.log.save()
        self.assertEqual( unicode(self.log),  u"Gps Application log at 2010-01-01 15:00:01")

    def test_list_app(self):
        """ Tests application listing. """
        login = self.do_login()
        response = self.client.get('/applications/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gps Application</a></td>")
        self.assertContains(response, "<tr>", 2) # 1 app, plus header
        
    def test_detail_app(self):
        """ Tests the application page. """
        response = self.client.get('/applications/%s/' % self.gps.id )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gps Application")
        self.assertContains(response, "Edit Application",0)
        
        login = self.do_login()
        response = self.client.get('/applications/%s/' % self.gps.id )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Application",1)

    def test_requires_login_to_add_app(self):
        """ Tests the login requirement for the add application page. """
        response = self.client.get('/applications/add/')
        self.assertEqual(response.status_code, 302) # redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/applications/add/')
    
    def test_add_app(self):
        """ Tests the application insersion. """
        login = self.do_login()
        response = self.client.get('/applications/add/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add Application")
        self.assertContains(response, "<form", 1)
        self.assertContains(response, "I agree to ") # terms of service.

        zf = open(relative('../../tests/python_test_app.zip'),'rb')
        pf = open(relative('../../tests/wmlogo.png'),'rb')
        post_data = {
            'name': 'Example App',
            'zipfile': zf,
            'icon': pf,
            'category': self.educational.id, 
            'description': "Example app",
            'tos': False
        }
        
        # Test without TOS
        response = self.client.post('/applications/add/', post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have to agree')
        
        # Move file pointers to the beginning of a file
        map(lambda x: x.seek(0), [zf, pf])
        
        post_data['tos'] = True
        response = self.client.post('/applications/add/', post_data)
        map(lambda x: x.close(), [zf, pf])
        
        
        self.assertEqual(Application.objects.filter(name='Example App').count(), 1)
        self.assertRedirects(response, '/applications/%s/' % Application.objects.get(name='Example App').id)
        response = self.client.get('/applications/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Example App</a></td>")
        
    def test_upload_app(self):
        """ Tests the Upload of a Zip file through the SWFUpload method. """
        login = self.do_login()

        zf = open(relative('../../tests/python_test_app.zip'),'rb')
        response = self.client.post('/applications/upload/?user_id=%s' % self.zacarias.id, {
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
            'description': "Example app",
            'tos':True
        }
        c = Application.objects.count()
        response = self.client.post('/applications/add/', post_data)
        self.assertEqual(c+1, Application.objects.count())
        self.assertRedirects(response, '/applications/%s/' % Application.objects.get(name='Yet another App').id)
        os.remove(relative('../../media/applications', name))

    def test_get_unique_path(self):
        """ Tests if get_unique_path works. """
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
        """ Tests login requirements for edit application. """
        response = self.client.get('/applications/%s/edit/' % self.gps.id)
        self.assertEqual(response.status_code, 302) # redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/applications/%s/edit/' % self.gps.id)

    def test_edit_app(self):
        """ Tests edit application page. """
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
        """ Tests delete application page. """
        c = Application.objects.count()
        login = self.do_login()
        response = self.client.get('/applications/%s/delete/' % self.gps.id)
        self.assertRedirects(response, '/applications/')
        self.assertEqual(c-1, Application.objects.count())

    def test_requires_staff_to_remove_app(self):
        """ Tests administration permition to remove application. """
        c = Application.objects.count()
        login = self.do_login()
        response = self.client.get('/applications/%s/remove/' % self.gps.id)
        self.assertRedirects(response, '/accounts/login/?next=/applications/%s/remove/'% self.gps.id)
        self.assertEqual(c, Application.objects.count())
        
    def test_remove_app(self):
        """ Tests remove application by admin. """
        # Clean email inbox
        mail.outbox = []
        
        c = Application.objects.count()
        login = self.do_admin_login()
        response = self.client.get('/applications/%s/remove/' % self.gps.id)
        self.assertRedirects(response, '/applications/')
        self.assertEqual(c-1, Application.objects.count())
        
        self.assertEquals(len(mail.outbox), 1)
        self.assertTrue("Application removed from the wall" in mail.outbox[0].subject)
    
    
    def test_authorized_list_cat(self):
        """ Test category list page. """
        login = self.do_admin_login()
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Games</td>")
        self.assertContains(response, "<tr>", Category.objects.count()+1) # 2 cat, plus header
    
    def test_authorized_add_category(self):
        """ Test category insersion page. """
        c = Category.objects.count()
        login = self.do_admin_login()
        post_data = {
            'name': 'Action'
        }
        response = self.client.post('/categories/add/', post_data)
        self.assertRedirects(response, '/categories/')
        self.assertEqual(c+1, Category.objects.count())

    def test_unauthorized_add_category(self):
        """ Tests permition to add category. """
        c = Category.objects.count()
        login = self.do_login()
        post_data = {
            'name': 'Action'
        }
        response = self.client.post('/categories/add/', post_data)
        self.assertRedirects(response, '/accounts/login/?next=/categories/add/')
        self.assertEqual(c, Category.objects.count())

    def test_edit_cat(self):
        """ Test category edition. """
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
        """ Test removal of empty category. """
        login = self.do_admin_login()
        c = Category.objects.count()
        response = self.client.post('/categories/%s/remove/'%self.games.id)
        self.assertRedirects(response, '/categories/')
        self.assertEqual(c-1, Category.objects.count())

    def test_remove_used_cat(self):
        """ Test removal of non-empty category. """
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
        """ Test existence of default category. """
        self.assertEqual(Category.objects.filter(name=DEFAULT_CATEGORY).count(), 1)
    
    def test_register_with_different_passwords(self):
        """ Test different passwords in register form. """
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
        """ Tests email restrictions in register form. """
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
        """ Tests register form without any password. """
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
        """ Test register form. """
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
  
    def test_application_log_limit(self):
        """ Test if application log is deleting element besides the limit. """
        for i in range(10):
            ApplicationLog.objects.create(application = self.gps, error_description="Debug %s" % i)
        
        self.assertEqual(ApplicationLog.objects.count(), APPS_MAX_LOG_ENTRIES)
                
    def test_report_abuse(self):
        """ Tests for a sample abuse report """
        # Clean email inbox
        mail.outbox = []
        
        login = self.do_login()
        response = self.client.get('/applications/%s/' % self.gps.id )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Report abuse")
        self.assertContains(response, "<form", 1)
        self.assertContains(response, "abuse_description")
        self.assertContains(response, "submit")
        
        sample_abuse_description = 'This application contains some sort of innapropriate content.'
        post_data = {
            'abuse_description': sample_abuse_description,
        }
        response = self.client.post('/applications/%s/report_abuse/' % self.gps.id, post_data)
        self.assertRedirects(response, '/applications/')
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].to), 1)
        self.assertEqual(mail.outbox[0].to[0], get_contact_admin_email())
        self.assertEqual(mail.outbox[0].subject, '[WallManager] Application ' + self.gps.name + ' received an abuse report.')
        self.assertTrue( sample_abuse_description in mail.outbox[0].body)
        self.assertTrue( self.gps.name in mail.outbox[0].body)

    def test_documentation_edit(self):
        login = self.do_admin_login()
        #test the menu
        c = FlatPage.objects.count()
        response = self.client.post('/documentation/menu/')
        self.assertContains(response, ">edit</a>", Category.objects.count()) 

        #update documentation 
        post_data = {
            'content': 'New content.',
            'title': 'Documents'
        }
        response = self.client.post('/documentation/1/edit/', post_data)
        f = FlatPage.objects.get(title='Documents')
        self.assertEqual(f.content, "New content.")
       
        #update faq 
        post_data = {
            'content': 'New faq content.',
            'title': 'FaqDocuments'
        }
        response = self.client.post('/documentation/2/edit/', post_data)
        f = FlatPage.objects.get(title='FaqDocuments')
        self.assertEqual(f.content, "New faq content.")
        #update tech documentation 
        post_data = {
            'content': 'New tech content.',
            'title': 'TDocuments'
        }
        response = self.client.post('/documentation/3/edit/', post_data)
        f = FlatPage.objects.get(title='TDocuments')
        self.assertEqual(f.content, "New tech content.")
        
    
    def tearDown(self):
        pass
