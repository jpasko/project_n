from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

def upload_to_photo(instance, filename):
    """
    Creates an upload_to path for photos.
    """
    return 'images/%s/%s' % (instance.gallery.user.id, filename)

def upload_to_profile_photo(instance, filename):
    """
    Same, but for profile photos.
    """
    return 'images/%s/%s' % (instance.user.id, filename)

class Gallery(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=75, blank=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return u'User: %s, Title: %s' % (self.user.username, self.title)

class Photo(models.Model):
    gallery = models.ForeignKey(Gallery)
    image = ProcessedImageField([ResizeToFit(width=640,
                                             height=640,
                                             upscale=False)],
                                upload_to=upload_to_photo)
    thumbnail = ImageSpecField([ResizeToFill(50, 50)],
                               image_field='image')
    caption = models.CharField(max_length=140, blank=True)

    def __unicode__(self):
        return u'Image for %s' % self.gallery.title

class ProfilePhoto(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to=upload_to_profile_photo)

    def __unicode__(self):
        return u'Profile image for %s' % self.user.username
