from django.test import TestCase
import models

class CreateUsers(TestCase):
    def test_user_creation(self):
        #Tests that 1 + 1 always equals 2.
        #self.failUnlessEqual(1 + 1, 2)
		
		#Creates usernames for Miguel Martins and Mario Zenha-Rela
		self.miguelmartins = models.User.objects.create(username="marm@student.dei.uc.pt", usertype="REGULAR USER", isbanned=False)
		self.mzr = models.User.objects.create(username="mzr@dei.uc.pt", usertype="ADMIN", isbanned=False)
		#Assertions for Miguel Martins
		self.failUnlessEqual(self.miguelmartins.username, "marm@student.dei.uc.pt")
		self.failUnlessEqual(self.miguelmartins.usertype, "REGULAR USER")
		self.failUnlessEqual(self.miguelmartins.isbanned, False)
		#Assertions for Mario Zenha-Rela
		self.failUnlessEqual(self.mzr.username, "mzr@dei.uc.pt")
		self.failUnlessEqual(self.mzr.usertype, "ADMIN")
		self.failUnlessEqual(self.mzr.isbanned, False)
		#There should now be 2 users in the database
		self.number_of_users = len(models.User.objects.all())
		self.failUnlessEqual(self.number_of_users, 2)
		
class CreateCategories(TestCase):
	def test_category_creation(self):
		self.educational = models.Category.objects.create(name="EDUCATIONAL")
		self.games = models.Category.objects.create(name="GAMES")
		self.failUnlessEqual(self.educational.name, "EDUCATIONAL")
		self.failUnlessEqual(self.games.name, "GAMES")
		
class CreateApplications(TestCase):
	def test_application_creation(self):
		#Fetch the users from the database
		self.miguelmartins = models.User.objects.filter(username="marm@student.dei.uc.pt")
		self.mzr = models.User.objects.filter(username="mzr@dei.uc.pt")
		#There should only be 2 users
		self.failUnlessEqual(len(self.miguelmartins), 1)
		self.failUnlessEqual(len(self.mzr), 1)
		#Fetch the two categories
		self.educational = models.Category.objects.filter(name="EDUCATIONAL")
		self.games = models.Category.objects.filter(name="GAMES")
		#Create applications
		self.gpsapplication = models.Application.objects.create(name="GPS APPLICATION", appowner=self.mzr, category=self.educational, like=0, dislike=0)