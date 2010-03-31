from django.db import models

class User(models.Model):
    email = models.EmailField()
    is_admin = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"%s" % self.email
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return u"%s" % self.name

class Application(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    zipfile = models.FileField(upload_to='applications')
    icon = models.FileField(upload_to='icons')
    extraction_path = models.FilePathField()
    
    def value(self):
        """ The value of an application, based on the likes and disliked """
        return self.likes - self.dislikes
        
    class Meta:
        ordering = ("-likes",)
    
    def __unicode__(self):
        return u"%s" % self.name
    
    
class AbuseReport(models.Model):
    application = models.ForeignKey(Application)
    author = models.ForeignKey(User)
    description = models.TextField()

    def __unicode__(self):
        return u"%s reported by %s" % (self.application, self.author)
    
    
class AuthConfig(models.Model):
    contact = models.EmailField()
    superadmin = models.IntegerField()
    
    class Meta:
        verbose_name = "Global Configuration"
        verbose_name_plural = "Global Configurations"
    
class ProjectorControl(models.Model):
    inactivity_time = models.IntegerField()
    shutdown_time = models.TimeField()
    startup_time = models.TimeField()
