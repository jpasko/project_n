from accounts.models import UserProfile
from portfolios.models import Item, Photo, Video, Gallery
from django import forms

class UserProfileForm(forms.ModelForm):
    """
    Form to edit a portfolio.
    """
    class Meta:
        model = UserProfile
        exclude = ('user',
                   'photo_count',
                   'allow_contact',
                   'allow_about',
                   'location',
                   'email',
                   'about',
                   'phone',
                   'website',
                   'twitter',
                   'facebook',
                   'google_plus',
                   'linkedin',)

class UploadItemForm(forms.ModelForm):
    """
    Form to upload a generic item.
    """
    class Meta:
        model = Item
        exclude = ('order', 'is_photo', 'gallery')

class UploadPhotoForm(forms.ModelForm):
    """
    Form to upload a photo into a gallery.
    """
    class Meta:
        model = Photo
        exclude = ('item')

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

class EditItemForm(forms.ModelForm):
    """
    Allows the user to edit the caption on their item.
    """
    class Meta:
        model = Item
        exclude = ('order', 'gallery', 'is_photo')

class EditGalleryForm(forms.ModelForm):
    """
    Allows the user to edit their gallery.
    """
    class Meta:
        model = Gallery
        exclude = ('user', 'count', 'order')
