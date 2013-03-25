from accounts.models import UserProfile
from portfolios.models import Item, Photo, Video, Gallery
from django import forms

class UserProfileForm(forms.ModelForm):
    """
    Form to edit a portfolio.
    """
    class Meta:
        model = UserProfile
        widgets = { 
            'blog': forms.TextInput(attrs={'placeholder': 'URL (include http://)'}),
            'blog_name': forms.TextInput(attrs={'placeholder': 'Name'}),
        }  
        exclude = ('user',
                   'photo_count',
                   'allow_about',
                   'location',
                   'email',
                   'about',
                   'phone',
                   'website',
                   'blogger',
                   'deviantart',
                   'digg',
                   'facebook',
                   'flickr',
                   'google_plus',
                   'linkedin',
                   'myspace',
                   'orkut',
                   'pinterest',
                   'tumblr',
                   'twitter',
                   'wordpress',
                   'youtube',
                   'edit_mode',)

class ProfilePictureForm(forms.ModelForm):
    """
    Form to edit or delete the profile picture.
    """
    class Meta:
        model = UserProfile
        exclude = ('user',
                   'photo_count',
                   'contact_type',
                   'allow_about',
                   'enable_banner',
                   'show_get_started',
                   'page_width',
                   'title_size',
                   'font_size',
                   'font_type',
                   'thumbnail_dimension',
                   'ga_1',
                   'ga_2',
                   'copy_text',
                   'fullname',
                   'location',
                   'email',
                   'about',
                   'phone',
                   'background_color',
                   'text_color',
                   'text_color_hover',
                   'website',
                   'blog',
                   'blog_name',
                   'blogger',
                   'deviantart',
                   'digg',
                   'facebook',
                   'flickr',
                   'google_plus',
                   'linkedin',
                   'myspace',
                   'orkut',
                   'pinterest',
                   'tumblr',
                   'twitter',
                   'wordpress',
                   'youtube',
                   'banner',
                   'edit_mode',)

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
    delete_current_thumbnail = forms.CharField()
    class Meta:
        model = Gallery
        exclude = ('user', 'count', 'order')
