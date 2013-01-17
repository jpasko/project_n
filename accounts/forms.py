import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from accounts.models import UserProfile

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput()
    )

    def clean(self):
        """
        Overrides the clean method to do password validation.
        """
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            # Only do something if both fields are valid so far.
            if password1 != password2:
                raise forms.ValidationError('Passwords must match.')
            # Always return the full collection of cleaned data.
            return cleaned_data

    def clean_username(self):
        """
        Checks that the username is valid and unique.
        """
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric '
                                        'characters')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError(u'%s already taken.' % username)

    def clean_email(self):
        """
        Checks that the email is unique.
        """
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('Email already taken')

class PaidRegistrationForm(RegistrationForm):
    """
    Form for accepting credit cards.
    """
