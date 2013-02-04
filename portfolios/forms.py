from accounts.models import UserProfile
from portfolios.models import Photo, Gallery
from django import forms
from imagekit.models.fields import ProcessedImageField

class UserProfileForm(forms.ModelForm):
    """
    Form to edit a portfolio.
    """
    class Meta:
        model = UserProfile
        exclude = ('account_type', 'user', 'photo_count')
        widgets = {
            'picture': forms.FileInput(),
        }

class UploadPhotoForm(forms.ModelForm):
    """
    Form to upload a photo into a gallery.
    """
    class Meta:
        model = Photo
        exclude = ('order')

class CreateGalleryForm(forms.ModelForm):
    """
    Form to create a gallery.
    """
    class Meta:
        model = Gallery
        exclude = ('user', 'count', 'order')

class EditPhotoForm(forms.ModelForm):
    """
    Allows the user to edit the caption on their photo.
    """
    class Meta:
        model = Photo
        exclude = ('order', 'gallery', 'image')

class EditGalleryForm(forms.ModelForm):
    """
    Allows the user to edit their gallery.
    """
    class Meta:
        model = Gallery
        exclude = ('user', 'count', 'order')
