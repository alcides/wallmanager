from django.db import models
from django.contrib.auth.models import User
from appman.utils import log_file

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return u"%s" % self.name

class Application(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    description = models.TextField(blank=True)
    
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    
    runs = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    
    zipfile = models.FileField(upload_to='applications')
    icon = models.ImageField(upload_to='icons')
    extraction_path = models.FilePathField()
    
    def value(self):
        """ The value of an application, based on the likes and dislikes """
        total = self.likes + self.dislikes
        if total != 0:
            return ( self.likes ) / float(total)
        else:
            return 0
        
    def stars(self):
        """ The number of stars an application has, based on the likes and dislikes """
        return round(self.value()*5)
            
    class Meta:
        ordering = ("-likes",)
    
    def __unicode__(self):
        return u"%s" % self.name
    
    def save(self, force_insert=False, force_update=False):
        application_was_edited = False
        try:
            old_obj = Application.objects.get(pk=self.pk)
            if old_obj.icon.path != self.icon.path:
                    old_obj.icon.delete()
            application_was_edited = True
        except:
            pass
        
        try:
            old_obj = Application.objects.get(pk=self.pk)
            if old_obj.zipfile.path != self.zipfile.path:
                    old_obj.zipfile.delete()
        except:
            pass
        
        super(Application, self).save(force_insert, force_update)
        if (application_was_edited):
            log_file.log_app_event(self, 'edited')
    
    @models.permalink
    def get_absolute_url(self):
        return ("application-detail", [str(self.id)])
        
class ProjectorControl(models.Model):
    inactivity_time = models.IntegerField()
    startup_time = models.TimeField()
    shutdown_time = models.TimeField()

    def save(self, *args, **kwargs):
        """ There can be only one ProjectorControl instance."""
        ProjectorControl.objects.all().delete()
        super(ProjectorControl,self).save(*args, **kwargs)
        
class ApplicationLog(models.Model):
    application = models.ForeignKey(Application)
    datetime = models.DateTimeField(auto_now_add=True)
    error_description = models.CharField(max_length=255)
    
    def __unicode__(self):
        return u"%s log at %s" % (self.application.name, self.datetime)