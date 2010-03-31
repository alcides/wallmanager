from django.test import TestCase
from appman.models import *

class ApplicationManagement(TestCase):
	
	def setUp(self):
		#Creates usernames for Zacarias and Mario Zenha-Rela
		self.zacarias = User.objects.create(email="zacarias@student.dei.uc.pt")
		self.mzr = User.objects.create(email="mzr@dei.uc.pt", is_admin=True)
		
		self.educational = Category.objects.create(name="Educational")
		self.games = Category.objects.create(name="Games")
	
		self.gps = Application.objects.create(name="Gps Application", owner=self.mzr, category=self.educational)
		
		self.abuse = AbuseReport.objects.create(author=self.zacarias, application=self.gps, description="I don't like that application. It has mature contet.")
	
	def test_models_representation(self):
		self.assertEqual( unicode(self.mzr), u"mzr@dei.uc.pt" )
		self.assertEqual( unicode(self.educational), u"Educational" )
		self.assertEqual( unicode(self.gps), u"Gps Application" )	
		self.assertEqual( unicode(self.abuse), u"Gps Application reported by zacarias@student.dei.uc.pt" )				
	
	def test_application_value(self):
	    self.gps.likes = 5
	    self.gps.dislikes = 3
	    self.gps.save()
	    self.assertEqual( self.gps.value(), 2)
	
		
	def tearDown(self):
		pass
