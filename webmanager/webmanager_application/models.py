from django.db import models

class User(models.Model):
    username = models.EmailField()
    usertype = models.CharField(max_length=12)
	isbanned = models.BooleanField()
	
class Category(models.Model):
	name = models.CharField()
	
class Application(models.Model):
	name = models.CharField()
	appowner = models.ForeignKey('User')
	category = models.ForeignKey('Category')
	like = models.IntegerField()
	dislike = models.IntegerField()
	zipfile = models.FileField(upload_to='applications')
	icon = models.FilePathField()
	extractionpath = models.FilePathField()
	
class AbuseReport(models.Model):
	appid = models.ForeignKey('Application')
	reportedby = models.ForeignKey('User')
	description = models.TextField()
	
class WallManager(models.Model):
	contact = models.EmailField()
	superadmin = models.IntegerField()
	
class ProjectorControl(models.Model):
	inactivitytime = models.IntegerField()
	shutdowntime = models.TimeField()
	startuptime = models.TimeField()