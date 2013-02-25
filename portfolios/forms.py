from accounts.models import UserProfile
from portfolios.models import Item, Photo, Video, Gallery
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

class UploadItemForm(forms.ModelForm):
    """
    Form to upload a generic item.
    """
    class Meta:
        model = Item
        exclude = ('order', 'is_photo')

class UploadPhotoForm(forms.ModelForm):
    """
    Form to upload a photo into a gallery.
    """
    class Meta:
        model = Photo
        exclude = ('order')

class UploadVideoForm(UploadItemForm):
    """
    Form to upload a video.
    """
    url = forms.URLField()

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
