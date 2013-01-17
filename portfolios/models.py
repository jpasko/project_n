from django.db import models
from django.contrib.auth.models import User

class Gallery(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=75, blank=True)

    def __unicode__(self):
        return u'User: %s, Title: %s' % (self.user.username, self.title)

class Photo(models.Model):
    gallery = models.ForeignKey(Gallery)
    image = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=140, blank=True)

    def __unicode__(self):
        return u'Image for %s' % self.gallery.title

class ProfilePhoto(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to='images/')

    def __unicode__(self):
        return u'Profile image for %s' % self.user.username
