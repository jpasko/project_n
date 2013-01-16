from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Attach a profile to the User model, and ensure that it's
# created whenever a new user is created.
class UserProfile(models.Model):
    # Required to associate with a unique user.
    user = models.OneToOneField(User)

    # The user's account type.
    account_type = models.CharField(max_length=1)

    # These are the free options.
    fullname = models.CharField(max_length=75)
    location = models.CharField(max_length=75)
    email = models.EmailField()

    # you must pay to use these ones.
    about = models.TextField()
    phone = models.CharField(max_length=20)
    picture = models.ImageField()
    

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
