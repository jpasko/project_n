from django.db import models
from django.contrib.auth.models import User

class Gallery(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return u'Gallery for %s' % self.user.username

class Photo(models.Model):
    #gallery = models.ForeignKey(Gallery)
    user = models.ForeignKey(User)
    caption = models.CharField(default='', max_length=140)
    image = models.ImageField(upload_to='images/')

    def __unicode__(self):
        return u'Image for %s' % self.gallery.title

class ProfilePhoto(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to='images/')

    def __unicode__(self):
        return u'Profile image for %s' % self.user.username
