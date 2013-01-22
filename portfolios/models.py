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

class Gallery(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=75, blank=True)
    count = models.IntegerField(default=0)
    order = models.IntegerField(null=True)

    # Static counter variable to set a unique order
    i = 0

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Override the save method to initialize the order field to be
        the primary key value.
        """
        if not self.id:
            self.order = Gallery.i
            Gallery.i += 1
        super(Gallery, self).save(*args, **kwargs)

class Photo(models.Model):
    gallery = models.ForeignKey(Gallery)
    image = ProcessedImageField([ResizeToFit(width=640,
                                             height=640,
                                             upscale=False)],
                                upload_to=upload_to_photo)
    thumbnail = ImageSpecField([ResizeToFill(250, 250)],
                               image_field='image')
    caption = models.CharField(max_length=140, blank=True)
    order = models.IntegerField()

    # Static counter variable to set a unique order
    i = 0

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return u'Image for %s' % self.gallery.title

    def save(self, *args, **kwargs):
        """
        Override the save method to initialize the order field to be
        the primary key value.
        """
        if not self.id:
            self.order = Photo.i
            Photo.i += 1
        super(Photo, self).save(*args, **kwargs)
