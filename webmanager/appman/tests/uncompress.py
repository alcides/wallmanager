from django.test import TestCase
from django.core import mail
from django.core.files import File

from appman.models import *
from appman.utils.uncompress import UncompressThread
from appman.utils.fileutils import relative

class UncompressTest(TestCase):
    def setUp(self):
        self.zacarias = User.objects.create_user(username="zacarias_stu", email="zacarias@student.dei.uc.pt", password="zacarias")
        self.educational = Category.objects.create(name="Educational")
        
    def test_zip_extraction(self):
        extract_folder = relative("../../tests/temp")
    
        # Clean email inbox
        mail.outbox = []
    
        app = Application.objects.create(name="E-mail Testing", owner=self.zacarias, category=self.educational)
        app.zipfile = File(open(relative("../../tests/python_test_app.zip")))
        app.save()
    
        thread = UncompressThread(Application, app, extract_folder)
        thread.run()
    
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, '[WallManager] Application successfully deployed')
        self.assertEquals(len(mail.outbox[0].to), 1)
        self.assertEquals(mail.outbox[0].to[0], 'zacarias@student.dei.uc.pt')
        self.assertEquals(mail.outbox[0].body, 'Your application, ' + app.name + ', has been successfully deployed.')
    
        # Clean extracted folder
        import shutil
        shutil.rmtree(extract_folder)