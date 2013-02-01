import subprocess
from os.path import join

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete

from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFit

from zebra.models import StripeCustomer

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
    location = models.CharField(verbose_name='location',
                                max_length=75,
                                blank=True)
    email = models.EmailField(verbose_name='contact email',
                              blank=True)
    about = models.TextField(verbose_name='about',
                             blank=True)
    phone = models.CharField(verbose_name='phone',
                             max_length=20, blank=True)

    STYLES = (
        ('D', 'Dark'),
        ('L', 'Light'),
        ('M', 'Minimalist'),
    )
    style = models.CharField(verbose_name='Background',
                             max_length=1,
                             choices=STYLES,
                             default='L')

    COLUMNS = (
        (3, 'Square'),
        (1, 'Wide'),
    )
    portfolio_columns = models.IntegerField(verbose_name='Portfolio thumbnail style',
                                            choices=COLUMNS,
                                            default=3)

    gallery_columns = models.IntegerField(verbose_name='Gallery thumbnail style',
                                          choices=COLUMNS,
                                          default=3)

    website = models.URLField(max_length=200, blank=True)

    picture = ProcessedImageField([ResizeToFit(width=200,
                                               height=250,
                                               upscale=False)],
                                  upload_to=upload_to,
                                  blank=True,
                                  null=True,
                                  verbose_name='Profile picture')
    
    def __unicode__(self):
        return u'Profile for %s' % self.user.username

# Create a Customer entry whenever a User is created.
class Customer(StripeCustomer):
    # Required to associate with a unique user.
    user = models.OneToOneField(User)
    ACCOUNT_LIMITS = (
        (settings.FREE_IMAGE_LIMIT, 'Starter (' + str(settings.FREE_IMAGE_LIMIT) + ' image uploads)'),
        (settings.PREMIUM_IMAGE_LIMIT, 'Premium (' + str(settings.PREMIUM_IMAGE_LIMIT) + ' image uploads)'),
        (settings.PROFESSIONAL_IMAGE_LIMIT, 'Professional (' + str(settings.PROFESSIONAL_IMAGE_LIMIT) + ' image uploads)'),
    )
    account_limit = models.IntegerField(verbose_name='Account type',
                                        choices=ACCOUNT_LIMITS,
                                        default=settings.FREE_IMAGE_LIMIT)

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
    Deletes the profile picture from the storage system upon UserProfile deletion.
    """
    instance.picture.delete(save=False)

# On the User save signal, create a UserProfile and a Customer.
post_save.connect(create_user_profile, sender=User)
post_save.connect(create_customer, sender=User)

# When deleting a UserProfile, be sure to delete the profile picture.
post_delete.connect(delete_profile_picture, sender=UserProfile)
