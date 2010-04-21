from models import ApplicationLogProxy, ApplicationProxy, CategoryProxy, UserProxy
from django.test import TestCase
from settings import APPS_MAX_LOG_ENTRIES
from unittest import TestLoader, TextTestRunner
from mtmenu import application_running

class TestMultiTouch(TestCase):
    """ Tests defined to the Wall Application 
    NOTE: Some tests take several time sleeping to assure the system calls are performed
    before the test asserts """

    def setUp(self):
        """ Sets up the database to have one user and one application """
        self.user = UserProxy.objects.create(username = "username",
                                             email = "username@email.com",
                                             password = "password")
        self.games = CategoryProxy.objects.create(name="GamesCategory")
        self.tetris = ApplicationProxy.objects.create(name="Tetris Game App",
                                                      owner=self.user,
                                                      category=self.games)

    def test_application_log_add (self):
        """ Tests to add some log messages to an application log """
        log_message1 = "Log message 1 (one)"
        log_message2 = "Log message 2 (two)"
        self.tetris.add_log_entry(log_message1)
        self.tetris.add_log_entry(log_message2)
        
        logs = ApplicationLogProxy.objects.filter(application = self.tetris)
        
        self.assertEqual(logs[logs.count() - 1].error_description, log_message2)

        
    def test_application_log_add_more_than_max_entries (self):
        """ add several logs above the max allowed to an application and checks if the last inserted are kept """
        
        max = APPS_MAX_LOG_ENTRIES
        added = 0
        
        # Add 4 more log entries than the max allowed
        for index in range(1, max + 4):
            self.tetris.add_log_entry('debug_msg%i' % index)
            added += 1
        
        # Get total entries stored on database
        total = ApplicationLogProxy.objects.filter(application = self.tetris).count()
        
        # Total shouldn't be higher that the max allowed
        self.assertEqual(total, max)
        
        # Verifies if the last APPS_MAX_LOG_ENTRIES are correct
        entries = ApplicationLogProxy.objects.order_by('-error_description').filter(application = self.tetris)
        
        for entry in entries:
            self.assertEqual(entry.error_description, 'debug_msg%i' % added)
            added -= 1
            if (added == max): break
            
            
    
    def test_run_application(self):
        """ tests running an application """
        self.tetris.execute()
        
        import time
        time.sleep(5)
        
        import application_running
        app = application_running.getAppRunning()
        
        self.assertNotEqual(app, None)
        self.assertEqual(app.poll(), None)
    
    
    def test_terminate_application(self):
        """ Kills the running application (if none runnig, it starts it) """
        import application_running
        import time
        
        if (not application_running.isAppRunning()):
            self.tetris.execute()
            time.sleep(5)
            
        app = application_running.getAppRunning()
        
        # guarantee the application is running
        self.assertNotEqual(app, None)

        application_running.killAppRunning()
         
        time.sleep(5)
        
        self.assertNotEqual(app.poll(), None)
    
    def tearDown(self):
        pass
    

if __name__ == '__main__':
    tests = TestLoader().loadTestsFromTestCase(TestMultiTouch)
    TextTestRunner(verbosity = 2).run(tests)
    