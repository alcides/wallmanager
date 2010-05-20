from datetime import time

from django.core import mail
from django.contrib.flatpages.models import FlatPage

from appman.utils import get_contact_admin_email
from appman.models import *
from appman.signals import *

from base import *

class AdminTest(BaseTest):
    def test_uniqueness_control(self):
        """ Tests uniqueness of the Projector Control object. """
        c1 = ProjectorControl.objects.create(inactivity_time=1, startup_week_time=time(1), shutdown_week_time=time(2), startup_weekend_time=time(2), shutdown_weekend_time=time(2))
        c2 = ProjectorControl.objects.create(inactivity_time=1, startup_week_time=time(1), shutdown_week_time=time(2), startup_weekend_time=time(2), shutdown_weekend_time=time(2))
        self.assertEqual( ProjectorControl.objects.count(), 1)
    
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

    def test_manage_admin(self):
        def add_admin(email, type, expected_response):
            post_data = {
                'email': email,
                'type':  type,
            }
            response = self.client.post('/admins/',post_data)
            self.assertContains(response, expected_response)
        
        # Power administrator login
        self.do_admin_login()
        
        # Using alfredo since he is a normal user
        self.assertEqual(self.alfredo.is_staff, False)
        self.assertEqual(self.alfredo.is_superuser, False)
        
        # Add him as a normal administrator
        add_admin(self.alfredo.email, 'Normal', 'Administrator added.')
        self.alfredo = User.objects.get(id=self.alfredo.id)
        self.assertEqual(self.alfredo.is_staff, True)
        self.assertEqual(self.alfredo.is_superuser, False)
        
        # Add him as a power administrator
        add_admin(self.alfredo.email, 'Power', 'Administrator added.')
        self.alfredo = User.objects.get(id=self.alfredo.id)
        self.assertEqual(self.alfredo.is_staff, True)
        self.assertEqual(self.alfredo.is_superuser, True)
        
        # Remove him from being an administrator
        response = self.client.get('/admins/%d/remove/' % self.alfredo.id)
        self.assertRedirects(response, '/admins/')
        self.alfredo = User.objects.get(id=self.alfredo.id)
        self.assertEqual(self.alfredo.is_staff, False)
        self.assertEqual(self.alfredo.is_superuser, False)
        
        # Test adding a non-user as admin
        add_admin('lololololol@student.dei.uc.pt', 'Normal', 'is not registered')


