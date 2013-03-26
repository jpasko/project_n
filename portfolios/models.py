import subprocess
from os.path import join

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.conf import settings
from django.contrib.auth.models import User

from imagekit.models import ImageSpecField
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit, SmartResize

def upload_to_photo(instance, filename):
    """
    Creates an upload_to path for photos.
    """
    return 'photos/%d/%s' % (instance.item.gallery.id, filename)

def upload_to_gallery(instance, filename):
    """
    Creates an upload_to path for photos.
    """
    return 'thumbnails/%d/%s' % (instance.user.id, filename)

class Gallery(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=75, blank=True)
    count = models.IntegerField(default=0)
    order = models.IntegerField(default=9999, blank=True)
    thumbnail = ProcessedImageField([SmartResize(width=settings.THUMBNAIL_WIDTH,
                                                 height=settings.THUMBNAIL_HEIGHT)],
                                    upload_to=upload_to_gallery,
                                    blank=True,
                                    null=True,
                                    verbose_name='Optional thumbnail')

    class Meta:
        ordering = ['order', 'pk']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Override save to delete the old thumbnail.
        """
        try:
            this = Gallery.objects.get(pk=self.id)
            if this.thumbnail and this.thumbnail != self.thumbnail:
                this.thumbnail.delete(save=False)
        except: pass
        super(Gallery, self).save(*args, **kwargs)

class Item(models.Model):
    gallery = models.ForeignKey(Gallery)
    is_photo = models.BooleanField(default=True)
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=9999, blank=True)

    class Meta:
        ordering = ['order', 'pk']

class Photo(models.Model):
    item = models.OneToOneField(Item)
    image = ProcessedImageField([ResizeToFit(width=settings.IMAGE_WIDTH,
                                             height=settings.IMAGE_HEIGHT,
                                             upscale=False)],
                                upload_to=upload_to_photo)
    thumbnail = ImageSpecField([SmartResize(settings.THUMBNAIL_WIDTH, settings.THUMBNAIL_HEIGHT)],
                               image_field='image')

class Video(models.Model):
    item = models.OneToOneField(Item)
    url = models.URLField(verbose_name="YouTube, Vimeo, or Dailymotion URL")

def delete_photo(sender, instance, *args, **kwargs):
    """
    Deletes the image from the file system upon Photo deletion.
    """
    if instance.image:
        instance.image.delete(save=False)

def delete_gallery(sender, instance, *args, **kwargs):
    """
    Deletes the thumbnail from the file system upon Gallery deletion.
    """
    if instance.thumbnail:
        instance.thumbnail.delete(save=False)

# Connect the delete methods to the post_delete signals.
post_delete.connect(delete_photo, sender=Photo)
post_delete.connect(delete_gallery, sender=Gallery)
