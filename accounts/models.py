from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFit

def upload_to(instance, filename):
    """
    Upload path for profile photos.
    """
    return 'images/%s/%s' % (instance.user.id, filename)

# Attach a profile to the User model, and ensure that it's
# created whenever a new user is created.
class UserProfile(models.Model):
    # Required to associate with a unique user.
    user = models.OneToOneField(User)

    # The number of photos owned by this user.
    photo_count = models.IntegerField(default=0)

    # The user's account type.
    ACCOUNT_TYPES = (
        ('F', 'Starter'),
        ('P', 'Premium'),
        ('R', 'Professional'),
    )
    account_type = models.CharField(max_length=1,
                                    choices=ACCOUNT_TYPES,
                                    default='F')

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
                                  verbose_name='Profile picture')
    
    def __unicode__(self):
        return u'Profile for %s' % self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    """
    Method to create a UserProfile to be associated with a User.
    """
    if created:
        UserProfile.objects.create(user=instance, fullname=instance.username)

# On the User save signal, create a UserProfile.
post_save.connect(create_user_profile, sender=User)
