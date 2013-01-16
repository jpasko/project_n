from django.db import models
from django.contrib.auth.models import User

class Gallery(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return u'Gallery for %s' % self.user.username

class Image(models.Model):
    gallery = models.ForeignKey(Gallery)
    caption = models.CharField(default='', max_length=140)
    upload_path = 'images/'
    image = models.ImageField(upload_to='images/')

    def __unicode__(self):
        return u'Image for %s' % self.gallery.title

class ProfileImage(models.Model):
    user = models.ForeignKey(User)
    image = models.ImageField(upload_to='images/')

    def __unicode__(self):
        return u'Profile image for %s' % self.user.username
