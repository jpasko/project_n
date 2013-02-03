import subprocess
from os.path import join

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.contrib.auth.models import User

from imagekit.models import ImageSpecField
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

def upload_to_photo(instance, filename):
    """
    Creates an upload_to path for photos.
    """
    return 'photos/%d/%s' % (instance.gallery.id, filename)

class Gallery(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=20, blank=True)
    count = models.IntegerField(default=0)
    order = models.IntegerField(default=9999, blank=True)

    class Meta:
        ordering = ['order', 'pk']

    def __unicode__(self):
        return self.title

class Photo(models.Model):
    gallery = models.ForeignKey(Gallery)
    image = ProcessedImageField([ResizeToFit(width=640,
                                             height=640,
                                             upscale=False)],
                                upload_to=upload_to_photo)
    # Thumbnail for the 3 column layout.
    thumbnail_3 = ImageSpecField([ResizeToFill(250, 250)],
                                 image_field='image')
    # Thumbnail for the 1 column layout
    thumbnail_1 = ImageSpecField([ResizeToFill(750, 250)],
                                 image_field='image')
    caption = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=9999, blank=True)

    class Meta:
        ordering = ['order', 'pk']

    def __unicode__(self):
        return u'Image for %s' % self.gallery.title

def delete_photo(sender, instance, *args, **kwargs):
    """
    Deletes the image from the file system upon Photo deletion.
    """
    if instance.image:
        instance.image.delete(save=False)

# When deleting a Photo, be sure to delete the image.
post_delete.connect(delete_photo, sender=Photo)
