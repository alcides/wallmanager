from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return u"%s" % self.name

    def delete(self):
        """ Deletes a category and moves apps to Default Category."""
        if self.name == settings.DEFAULT_CATEGORY:
            return
        
        defcat, g = Category.objects.get_or_create(name=settings.DEFAULT_CATEGORY)
        Application.objects.filter(category=self.id).update(category=defcat)

        super(Category,self).delete();
        
class Application(models.Model):
    name = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    description = models.TextField(blank=True)
    
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    
    runs = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    
    zipfile = models.FileField(upload_to=settings.ZIP_FOLDER)
    icon = models.ImageField(upload_to='icons')
    is_extracted = models.BooleanField(default=False)
    is_running = models.BooleanField(default=False)
    
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
        try:
            old_obj = Application.objects.get(pk=self.pk)
            if old_obj.icon.path != self.icon.path:
                    old_obj.icon.delete()
        except:
            pass
        
        try:
            old_obj = Application.objects.get(pk=self.pk)
            if old_obj.zipfile.path != self.zipfile.path:
                    old_obj.zipfile.delete()
        except:
            pass
        
        super(Application, self).save(force_insert, force_update)

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
    error_description = models.TextField(blank=True)
    
    def __unicode__(self):
        return u"%s log at %s" % (self.application.name, self.datetime)
        
class WallManager(models.Model):
    contact = models.EmailField(blank=True)
    
    def save(self, *args, **kwargs):
        """ There can be only one WallManager instance."""
        WallManager.objects.all().delete()
        super(WallManager,self).save(*args, **kwargs)
