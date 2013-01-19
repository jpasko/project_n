from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

def upload_to(instance, filename):
    """
    Creates an upload_to path for photos.
    """
    return 'images/%s/%s' % (instance.gallery.user.id, filename)

class Gallery(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=75, blank=True)
    description = models.TextField(blank=True)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class Photo(models.Model):
    gallery = models.ForeignKey(Gallery)
    image = ProcessedImageField([ResizeToFit(width=640,
                                             height=640,
                                             upscale=False)],
                                upload_to=upload_to)
    thumbnail = ImageSpecField([ResizeToFill(250, 250)],
                               image_field='image')
    caption = models.CharField(max_length=140, blank=True)
    position = models.IntegerField(default=0)

    def __unicode__(self):
        return u'Image for %s' % self.gallery.title
