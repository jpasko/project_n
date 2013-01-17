from accounts.models import UserProfile
from portfolios.models import Photo, Gallery, ProfilePhoto
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
    Form to upload a photo into a gallery.
    """
    class Meta:
        model = Photo

class UploadProfilePhotoForm(forms.ModelForm):
    """
    Form to upload a profile image.
    """
    class Meta:
        model = ProfilePhoto

class CreateGalleryForm(forms.ModelForm):
    """
    Form to create a gallery.
    """
    class Meta:
        model = Gallery
