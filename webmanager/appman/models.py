from django.db import models

class User(models.Model):
    LEVELS = (
        ('U', 'User'),
        ('A', 'Admin'),
        ('S', 'SuperAdmin'),
    )
    
    email = models.EmailField(unique=True)
    level = models.CharField(max_length=1, choices=LEVELS)
    
    
    def save(self, *args, **kwargs):
        """ Verifies is there is another superuser, and removes him from that level."""
        if self.level == 'S':
            User.objects.filter(level='S').update(level='A')
        super(User,self).save(*args, **kwargs)
    
    def __unicode__(self):
        return u"%s" % self.email
    
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
    
class ProjectorControl(models.Model):
    inactivity_time = models.IntegerField()
    shutdown_time = models.TimeField()
    startup_time = models.TimeField()
