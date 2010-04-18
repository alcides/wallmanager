from models import ApplicationLogProxy, ApplicationProxy, CategoryProxy, UserProxy
from django.test import TestCase
from settings import APPS_MAX_LOG_ENTRIES
from unittest import TestLoader, TextTestRunner

class TestMultiTouch(TestCase):

    def setUp(self):
        self.user = UserProxy.objects.create(username = "username",
                                             email = "username@email.com",
                                             password = "password")
        self.games = CategoryProxy.objects.create(name="GamesCategory")
        self.tetris = ApplicationProxy.objects.create(name="Tetris Game App",
                                                      owner=self.user,
                                                      category=self.games)

    def test_application_log_add (self):
        self.tetris.add_log_entry("Log message 1 (one)")
        self.tetris.add_log_entry("Log message 2 (two)")
        self.assertEqual(ApplicationLogProxy.objects.filter(application = self.tetris).count(), 2)

        
    def test_application_log_add_more_than_max_entries (self):
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
            
            
        
        
    def tearDown(self):
        pass
    

if __name__ == '__main__':
    tests = TestLoader().loadTestsFromTestCase(TestMultiTouch)
    TextTestRunner(verbosity = 2).run(tests)
    