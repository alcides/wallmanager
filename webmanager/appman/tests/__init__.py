import os
import re

from datetime import datetime, time
from django.core import mail
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.core.files import File
from django.db.models.signals import pre_save, post_save, post_delete

from appman.utils.fileutils import *
from appman.utils import get_contact_admin_email
from appman.utils.log_file import logger
from appman.utils.uncompress import UncompressThread
from appman.tests.uncompress import UncompressTest
from appman.models import *
from appman.signals import *

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
        # Zacarias is a user who uploads apps
        self.zacarias = User.objects.create_user(username="zacarias_stu", email="zacarias@student.dei.uc.pt", password="zacarias")
        
        # Alfredo is a visitor
        self.alfredo = User.objects.create_user(username="alfredo_stu", email="alfredo@student.dei.uc.pt", password="alfredo")
        
        # Prof. Plum is an admin for the app.
        self.plum = User.objects.create_user(username="plum_ede", email="plum@dei.uc.pt", password="plum")
        self.plum.is_staff = True
        self.plum.is_superuser = True
        self.plum.save()
        
        # Prof. Green is a regular admin.
        self.green = User.objects.create_user(username="green_ede", email="green@dei.uc.pt", password="green")
        self.green.is_staff = True
        self.green.is_superuser = False
        self.green.save()
        		
        self.educational = Category.objects.create(name="Educational")
        self.TestCat = Category.objects.create(name="TestCat")
        
        self.gps = Application.objects.create(name="Gps Application",description ="Some application", owner=self.zacarias, category=self.educational)
        
        self.logger = logger
        open(self.logger.fname, "w").write("\n")
        
    def do_login(self, user="zacarias"):
        """ Fakes login as standard user. """
        if user == "zacarias":
            login = self.client.login(username='zacarias_stu', password='zacarias')
        else:
            login = self.client.login(username='alfredo_stu', password='alfredo')
        self.assertEqual(login, True)
        return login

    def do_admin_login(self):
        """ Fakes login as administrator. """
        login = self.client.login(username='plum_ede', password='plum')
        self.assertEqual(login, True)
        return login
        
    def do_normal_admin_login(self):
        """ Fakes login as a normal administrator (as opposed to a super administrator). """
        login = self.client.login(username='green_ede', password='green')
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
        self.assertContains(response, "TestCat</td>")
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
        response = self.client.post('/categories/%s/remove/'%self.TestCat.id)
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
  
    def test_application_log_limit(self):
        """ Test if application log is deleting element besides the limit. """
        for i in range(10):
            ApplicationLog.objects.create(application = self.gps, error_description="Debug %s" % i)
        
        self.assertEqual(ApplicationLog.objects.count(), APPS_MAX_LOG_ENTRIES)
                
    def test_report_abuse(self):
        """ Tests for a sample abuse report """
        # Clean email inbox
        mail.outbox = []
        
        login = self.do_login(user="alfredo")
        response = self.client.get('/applications/%s/' % self.gps.id )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Report Abuse")
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

    def test_search_application(self):
        login = self.do_admin_login()
        self.app = Application.objects.create(name="Myapp", description="An application", owner=self.zacarias, category=self.educational)

        #test none app
        post_data = {
            'q':"Nothing else matters"
        }
        response = self.client.post('/applications/search/', post_data)
        self.assertContains(response, '<td>%s'%self.educational.name, 0) 

        #test search by title
        post_data = {
            'q':"My"
        }
        response = self.client.post('/applications/search/', post_data)
        self.assertContains(response, '<td>%s'%self.educational.name, 1) 
        
        #test search by description
        post_data = {
            'q':"Some"
        }
        response = self.client.post('/applications/search/', post_data)
        self.assertContains(response,  '<td>%s'%self.educational.name, 1) 
        
        

    def test_documentation_edit(self):
        """ Tests edition of documentation """
        login = self.do_admin_login()
        #test the menu
        c = FlatPage.objects.count()
        response = self.client.post('/documentation/menu/')
        exp = re.compile(r"\/documentation\/\d\/edit")
        self.assertEqual( len(exp.findall(response.content)), FlatPage.objects.count() )
        
        for page in FlatPage.objects.all():
            title = page.title
            post_data = { 'title': title, 'content': 'This is a new content.' }
            response = self.client.post('/documentation/%d/edit/' % page.id, post_data)
            f = FlatPage.objects.get(title=title)
            self.assertEqual(f.content, 'This is a new content.')    
            
    
    def test_logging(self):
        """ Tests logging capabilities """
        def check_contents(type_):
            contents = self.logger.retrieve_contents()
            self.assertTrue(type_ in contents)
         
        
        extract_folder = relative("../tests/temp")        
        temp_app = Application.objects.create(name="Temporary Application", owner=self.zacarias, category=self.educational, zipfile = File(open(relative("../../tests/python_test_app.zip"))))
        
        uncompress(Application, temp_app, post_save, **{'created':True})
        check_contents('added')
        
        thread = UncompressThread(Application, temp_app, extract_folder, extracted_email_signal)
        thread.run()
        check_contents('deployed')
                
        temp_app.name="Temporary Application 2"
        temp_app.extraction_path = extract_folder
        temp_app.save()
        uncompress(Application, temp_app, post_save, **{'created':False})        
        check_contents('edited')
        
        remove_app(Application, temp_app, post_delete)
        temp_app.delete()
        check_contents('deleted')
        check_contents('removed from filesystem')
                
    
    def test_application_logging(self):
        """ Tests the pages that show application logs. """
        login = self.do_login()

        # Create some dummy data
        app2 = Application.objects.create(name="Another Application",description ="Some application", owner=self.zacarias, category=self.educational)
        
        for i in range(5):
            app = i % 2 == 0 and self.gps or app2
            ApplicationLog.objects.create(application=app,
                error_description="Some error.")
        
        # test at application 1
        response = self.client.post('/applications/%s/log/' % app2.id)
        self.assertContains(response, '<p>Error Description:</p>', 2) 

        # test at application 2
        response = self.client.post('/applications/%s/log/' % self.gps.id)  
        self.assertContains(response, '<p>Error Description:</p>', 3) 
        
        # test invalid application
        response = self.client.post('/applications/23/log/')  
        self.assertRedirects(response, '/applications/')
        
    def test_category_filter(self):
        """ Tests if category filter works """
        login = self.do_login()
        self.games = Category.objects.get(name='Games')
        self.app = Application.objects.create(name="Myapp", description="An application", owner=self.zacarias, category=self.educational)
        self.app = Application.objects.create(name="Myapplication", description="An application", owner=self.zacarias, category=self.games)
        self.app = Application.objects.create(name="Otherapp", description="Another application", owner=self.plum, category=self.games)

        #confirm that the dropdown menu is correct
        c = Category.objects.count()
        response = self.client.get('/applications/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<option", c+1) 
        
        #filter my applications , this should return two applications
        post_data = {
            'category': '',
            'myApps': 'on'
        }
        response = self.client.post('/applications/filter/', post_data)  
        self.assertContains(response, '<td>%s'%(self.zacarias.username), 3) 
        #filter application by category
        post_data = {
            'category': self.educational.id,
            'myApps': 'off'
        }
        response = self.client.post('/applications/filter/', post_data)  
        self.assertContains(response, '<td>%s'%(self.educational.name), 2) 

        #filter application by category and owner
        post_data = {
            'category': self.games.id,
            'myApps': 'on'
        }

        response = self.client.post('/applications/filter/', post_data)  
        self.assertContains(response, '<td>%s'%(self.zacarias.username), 1) 
        

    def test_requires_superuser_to_define_contact_admin(self):
        """ Test superuser requirement in defining the contact administrator. """
        #Regular user
        login = self.do_login()
        response = self.client.get('/admins/contact/')
        self.assertRedirects(response, '/accounts/login/?next=/admins/contact/')
        #Admin
        login = self.do_normal_admin_login()
        response = self.client.get('/admins/contact/')
        self.assertRedirects(response, '/accounts/login/?next=/admins/contact/')
        
    def test_define_contact_admin(self):
        login = self.do_admin_login()
        response = self.client.get('/admins/contact/')
        #Make sure Mr. Green is listed as an admin and make him the new contact admin
        self.assertContains(response, '<option value="%s"' % self.green.email)
        post_data = {
            'contact_admin': 'green@dei.uc.pt',
        }
        response = self.client.post('/admins/contact/', post_data)
        self.assertContains(response, 'The contact admin was defined successfully.')
        #Remove Mr. Green from the admins (requires signal for contact admin update)
        post_delete.connect(check_if_contact_admin, sender=User)
        self.green.delete()
        response = self.client.get('/admins/contact/')
        self.assertContains(response, '<option value="%s"' % self.green.email, 0)
        post_delete.receivers = []


    def test_requires_login_to_contact(self):
        """ Tests login requirements for contacting the designated contact administrator. """
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 302) # redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/contact/')
        
    def test_contact(self):
        """ Sample test for a message to the designated contact administrator """
        # Clean email inbox
        mail.outbox = []
        
        login = self.do_login(user="zacarias")
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact Admin")
        self.assertContains(response, "<form", 1)
        self.assertContains(response, "message")
        self.assertContains(response, "submit")
        
        sample_message = 'I have an application that needs the library xyz. Could you please install it on the system?'
        post_data = {
            'message': sample_message,
        }
        response = self.client.post('/contact/', post_data)
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].to), 1)
        self.assertEqual(mail.outbox[0].to[0], get_contact_admin_email())
        self.assertEqual(mail.outbox[0].subject, '[WallManager] Message from user %s' % self.zacarias.email)
        self.assertTrue( sample_message in mail.outbox[0].body)

        
    def test_screensaver_time(self):
        def test_response(input, expected_content):
            post_data = {
                'screensaver_time': input,
            }
            response = self.client.post('/screensaver/', post_data)
            self.assertContains(response, expected_content)
            
            
        """ Tests the screensaver time setting. """
        login = self.do_admin_login()
        response = self.client.get('/screensaver/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ScreenSaver")
        self.assertContains(response, "<form", 1)
        self.assertContains(response, "screensaver_time")
        self.assertContains(response, "submit")
        
        correct_time = "01:05"
        #The following tests use several incorrect formats for submitting time, followed by one final, correct format
        test_response("abcd", 'Enter a valid time.')
        test_response("1234", 'Enter a valid time.')
        test_response("12 34", 'Enter a valid time.') #Missing one colon
        test_response("00:00", 'Time must be at least 00:01 (one minute).') #Must be larger than 00:00
        test_response("00:60", 'Enter a valid time.') #More than 59 minutes
        test_response("24:00", 'Enter a valid time.') #More than 23 hours (maximum is 23:59)
        test_response(correct_time, 'Screensaver inactivity time was set successfully.')
        
        time_in_database = ScreensaverControl.objects.all()[0].screensaver_inactivity_time
        self.assertEqual(str(time_in_database), correct_time + ":00")


    def tearDown(self):
        open(self.logger.fname, "w").write("\n")

        