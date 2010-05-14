import os
import re

from django.core import mail
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, post_delete

from appman.utils.log_file import logger
from appman.utils.fileutils import *
from appman.models import *
from appman.signals import *

DEFAULT_CATEGORY = "Others"
APPS_MAX_LOG_ENTRIES = 5

class BaseTest(TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        
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

    def tearDown(self):
        open(self.logger.fname, "w").write("\n")

