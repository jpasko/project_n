import subprocess
from os.path import join

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete

from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFit

def upload_to(instance, filename):
    """
    Upload path for profile photos.
    """
    return 'profile_photos/%d/%s' % (instance.id, filename)

# Attach a profile to the User model, and ensure that it's
# created whenever a new user is created.
class UserProfile(models.Model):
    # Required to associate with a unique user.
    user = models.OneToOneField(User)

    # The number of photos owned by this user.
    photo_count = models.IntegerField(default=0)

    # These are the free options.
    fullname = models.CharField(verbose_name='name',
                                max_length=75,
                                blank=True)
    location = models.CharField(verbose_name='location (optional)',
                                max_length=75,
                                blank=True)
    email = models.EmailField(verbose_name='contact email (optional)',
                              blank=True)
    about = models.TextField(verbose_name='about (optional)',
                             blank=True)
    phone = models.CharField(verbose_name='phone (optional)',
                             max_length=20, blank=True)

    STYLES = (
        ('D', 'Dark'),
        ('L', 'Light'),
    )
    style = models.CharField(verbose_name='Background',
                             max_length=1,
                             choices=STYLES,
                             default='L')

    COLUMNS = (
        (1, 'One'),
        (3, 'Three'),
    )
    portfolio_columns = models.IntegerField(verbose_name='Number of columns for your portfolio',
                                            choices=COLUMNS,
                                            default=3)

    gallery_columns = models.IntegerField(verbose_name='Number of columns within a gallery',
                                          choices=COLUMNS,
                                          default=3)

    website = models.URLField(max_length=200, blank=True)

    picture = ProcessedImageField([ResizeToFit(width=400,
                                               height=400,
                                               upscale=False)],
                                  upload_to=upload_to,
                                  blank=True,
                                  null=True,
                                  verbose_name='Profile picture')
    
    def __unicode__(self):
        return u'Profile for %s' % self.user.username

# Create a Customer entry whenever a User is created.
class Customer(models.Model):
    # Required to associate with a unique user.
    user = models.OneToOneField(User)
    image_limit = models.IntegerField(default=settings.FREE_IMAGE_LIMIT)
    stripe_id = models.CharField(max_length=255)
    ACCOUNT_TYPES = (
        ('F', 'Starter'),
        ('P', 'Premium'),
        ('R', 'Professional'),
    )
    account_type = models.CharField(max_length=1,
                                    choices=ACCOUNT_TYPES,
                                    default='F')

    def __unicode__(self):
        return u'Customer record for %s' % self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile to be associated with a User.
    """
    if created:
        UserProfile.objects.create(user=instance, fullname=instance.username)

def create_customer(sender, instance, created, **kwargs):
    """
    Create a Customer associated with a User.
    """
    if created:
        Customer.objects.create(user=instance)

def delete_profile_picture(sender, instance, *args, **kwargs):
    """
    Deletes the profile pictures from the file system upon User deletion.
    """
    directory = join(settings.MEDIA_ROOT, 'profile_photos', str(instance.id))
    subprocess.call(['rm', '-rf', directory])

# On the User save signal, create a UserProfile and a Customer.
post_save.connect(create_user_profile, sender=User)
post_save.connect(create_customer, sender=User)

# When deleting a User, be sure to delete the profile picture.
pre_delete.connect(delete_profile_picture, sender=User)
