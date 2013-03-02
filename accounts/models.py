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
    return 'profiles/%d/%s' % (instance.id, filename)

# Attach a profile to the User model, and ensure that it's
# created whenever a new user is created.
class UserProfile(models.Model):
    # Required to associate with a unique user.
    user = models.OneToOneField(User)

    photo_count = models.IntegerField(default=0)

    allow_contact = models.BooleanField(default=True)

    allow_about = models.BooleanField(default=True)

    full_width_navbar = models.BooleanField(default=False)

    page_width = models.IntegerField(default=940)

    ga_1 = models.IntegerField(null=True,
                               blank=True)
    ga_2 = models.IntegerField(null=True,
                               blank=True)

    fullname = models.CharField(verbose_name='name',
                                max_length=100,
                                blank=True)
    location = models.CharField(verbose_name='location',
                                max_length=100,
                                blank=True)
    email = models.EmailField(verbose_name='contact email',
                              blank=True)
    about = models.TextField(verbose_name='about',
                             blank=True)
    phone = models.CharField(verbose_name='phone',
                             max_length=100, blank=True)

    background_color = models.CharField(max_length=6,
                                        default='000000')

    text_color = models.CharField(max_length=6,
                                  default='999999')

    text_color_hover = models.CharField(max_length=6,
                                        default='D4D4D4')

    COLUMNS = (
        (3, 'Square'),
        (1, 'Wide'),
    )
    portfolio_columns = models.IntegerField(verbose_name='Thumbnail style',
                                            choices=COLUMNS,
                                            default=3)

    website = models.URLField(max_length=500, blank=True)
    blog = models.URLField(max_length=500, blank=True)

    twitter = models.URLField(max_length=500, blank=True)
    facebook = models.URLField(max_length=500, blank=True)
    google_plus = models.URLField(max_length=500, blank=True, verbose_name="Google+")
    linkedin = models.URLField(max_length=500, blank=True, verbose_name="LinkedIn")

    picture = ProcessedImageField([ResizeToFit(width=200,
                                               height=250,
                                               upscale=False)],
                                  upload_to=upload_to,
                                  blank=True,
                                  null=True,
                                  verbose_name='Profile picture')

    banner = ProcessedImageField([ResizeToFit(width=500,
                                              height=36,
                                              upscale=False)],
                                 upload_to=upload_to,
                                 blank=True,
                                 null=True,
                                 verbose_name='Banner')
    
    def __unicode__(self):
        return u'Profile for %s' % self.user.username

    def save(self, *args, **kwargs):
        """
        Override save to delete the old picture if a new one is uploaded.
        """
        try:
            this = UserProfile.objects.get(pk=self.id)
            if this.picture and this.picture != self.picture:
                this.picture.delete(save=False)
        except: pass
        super(UserProfile, self).save(*args, **kwargs)

# Create a Customer entry whenever a User is created.
class Customer(StripeCustomer):
    # Required to associate with a unique user.
    user = models.OneToOneField(User)
    ACCOUNT_LIMITS = (
        (settings.FREE_IMAGE_LIMIT, str(settings.FREE_IMAGE_LIMIT) + ' image uploads'),
        (settings.PREMIUM_IMAGE_LIMIT, str(settings.PREMIUM_IMAGE_LIMIT) + ' image uploads'),
        (settings.PROFESSIONAL_IMAGE_LIMIT, str(settings.PROFESSIONAL_IMAGE_LIMIT) + ' image uploads'),
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

def delete_banner_picture(sender, instance, *args, **kwargs):
    """
    Deletes the profile picture and banner from the storage system upon
    UserProfile deletion.
    """
    if instance.picture:
        instance.picture.delete(save=False)
    if instance.banner:
        instance.banner.delete(save=False)

# On the User save signal, create a UserProfile and a Customer.
post_save.connect(create_user_profile, sender=User)
post_save.connect(create_customer, sender=User)

# When deleting a UserProfile, be sure to delete the profile picture.
post_delete.connect(delete_banner_picture, sender=UserProfile)
