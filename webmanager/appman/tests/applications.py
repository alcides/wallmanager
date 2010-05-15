from datetime import datetime, time

from django.core.files import File
from django.core import mail

from appman.utils.fileutils import *
from appman.utils.uncompress import UncompressThread
from appman.models import *
from appman.signals import *

from base import *

class ApplicationTest(BaseTest):
    
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
        """ Tests the application search """
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
