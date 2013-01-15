from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Attach a profile to the User model, and ensure that it's
# created whenever a new user is created.
class UserProfile(models.Model):
    # Required to associate with a unique user.
    user = models.OneToOneField(User)

    # User profile follows:

    def __unicode__(self):
        return u'Profile for %s' % self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    """
    Method to create a UserProfile to be associated with a User.
    """
    if created:
        UserProfile.objects.create(user=instance)

# On the User save signal, create a UserProfile.
post_save.connect(create_user_profile, sender=User)
