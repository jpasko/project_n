import subprocess
from os.path import join

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.conf import settings
from django.contrib.auth.models import User

from imagekit.models import ImageSpecField
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

def upload_to_photo(instance, filename):
    """
    Creates an upload_to path for photos.
    """
    return 'photos/%d/%s' % (instance.gallery.id, filename)

def upload_to_gallery(instance, filename):
    """
    Creates an upload_to path for photos.
    """
    return 'thumbnails/%d/%s' % (instance.user.id, filename)

class Gallery(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=20, blank=True)
    count = models.IntegerField(default=0)
    order = models.IntegerField(default=9999, blank=True)
    thumbnail = ProcessedImageField([ResizeToFit(width=settings.WIDE_THUMBNAIL_WIDTH,
                                             height=settings.WIDE_THUMBNAIL_WIDTH,
                                             upscale=False)],
                                    upload_to=upload_to_gallery,
                                    blank=True,
                                    null=True,
                                    verbose_name='Optional thumbnail')
    # Thumbnail for the 3 column layout.
    thumbnail_3 = ImageSpecField([ResizeToFill(settings.SQUARE_THUMBNAIL_DIMENSION, settings.SQUARE_THUMBNAIL_DIMENSION)],
                                 image_field='thumbnail')
    # Thumbnail for the 1 column layout
    thumbnail_1 = ImageSpecField([ResizeToFill(settings.WIDE_THUMBNAIL_WIDTH, settings.WIDE_THUMBNAIL_HEIGHT)],
                                 image_field='thumbnail')

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

class Photo(models.Model):
    gallery = models.ForeignKey(Gallery)
    image = ProcessedImageField([ResizeToFit(width=750,
                                             height=750,
                                             upscale=False)],
                                upload_to=upload_to_photo)
    # Thumbnail for the 3 column layout.
    thumbnail_3 = ImageSpecField([ResizeToFill(settings.SQUARE_THUMBNAIL_DIMENSION, settings.SQUARE_THUMBNAIL_DIMENSION)],
                                 image_field='image')
    # Thumbnail for the 1 column layout
    thumbnail_1 = ImageSpecField([ResizeToFill(settings.WIDE_THUMBNAIL_WIDTH, settings.WIDE_THUMBNAIL_HEIGHT)],
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

def delete_gallery(sender, instance, *args, **kwargs):
    """
    Deletes the thumbnail from the file system upon Gallery deletion.
    """
    if instance.thumbnail:
        instance.thumbnail.delete(save=False)

# When deleting a Photo, be sure to delete the image.
post_delete.connect(delete_photo, sender=Photo)
post_delete.connect(delete_gallery, sender=Gallery)
