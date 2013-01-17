from accounts.models import UserProfile
from portfolios.models import Photo
from django import forms

class UserProfileForm(forms.ModelForm):
    """
    Form to edit a portfolio.
    """
    class Meta:
        model = UserProfile
        exclude = ('account_type', 'user')

class UploadPhotoForm(forms.ModelForm):
    """
    Form to upload a photo.
    """
    class Meta:
        model = Photo
