from django.core import mail
from django.core.files import File

from appman.utils.log_file import logger
from appman.models import *
from appman.signals import *

from base import *

class LoggingTest(BaseTest):

    def test_application_log_limit(self):
        """ Test if application log is deleting element besides the limit. """
        for i in range(10):
            ApplicationLog.objects.create(application = self.gps, error_description="Debug %s" % i)

        self.assertEqual(ApplicationLog.objects.count(), APPS_MAX_LOG_ENTRIES)        


    def test_logging(self):
        """ Tests logging capabilities """
        def check_contents(type_):
            contents = self.logger.retrieve_contents()
            self.assertTrue(type_ in contents)


        extract_folder = relative("../tests/temp")        
        temp_app = Application.objects.create(name="Temporary Application", owner=self.zacarias, category=self.educational, zipfile = File(open(relative("../../tests/python_test_app.zip"))))

        uncompress_file(Application, temp_app, post_save, **{'created':True})
        check_contents('added')

        thread = UncompressThread(Application, temp_app, extract_folder, extracted_email_signal)
        thread.run()
        check_contents('deployed')

        temp_app.name="Temporary Application 2"
        temp_app.extraction_path = extract_folder
        temp_app.save()
        uncompress_file(Application, temp_app, post_save, **{'created':False})        
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
