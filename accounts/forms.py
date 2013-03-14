import re
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from accounts.models import UserProfile, Customer

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs={'placeholder':'Username'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'placeholder':'Email'}))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder':'Password'})
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'placeholder':'Password (again)'})
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
                raise forms.ValidationError('These passwords must match!')
            # Always return the full collection of cleaned data.
            return cleaned_data

    def clean_username(self):
        """
        Checks that the username is valid and unique.
        Since the username doubles as a subdomain, it must contain only
        alphanumerics (lowercase) and the hyphen (-).
        """
        username = self.cleaned_data['username']
        if username in settings.RESERVED_TERMS:
            raise forms.ValidationError(u'That one\'s taken!')
        if not re.search(r'^(?!-)[a-z0-9\-]*(?<!-)$', username):
            raise forms.ValidationError(u'Lowercase alphanumerics only!')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError(u'That one\'s taken!')

    def clean_email(self):
        """
        Checks that the email is unique.
        """
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError(u'That one\'s taken!')

class CardForm(forms.Form):
    """
    Form for accepting credit cards.
    """
    stripe_token = forms.CharField(
        required = True,
        widget = forms.HiddenInput()
    )

    def addError(self, message):
        self._errors[NON_FIELD_ERRORS] = self.error_class([message])

class ChangeAccountForm(forms.ModelForm):
    """
    Form to upgrade/downgrade an existing user's account.
    """
    class Meta:
        model = Customer
        exclude = ('user', 'stripe_id')

class ContactForm(forms.Form):
    """
    Form for contact page.
    """
    sender = forms.EmailField(required=False)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':4}))
