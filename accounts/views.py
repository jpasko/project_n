from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from accounts.forms import RegistrationForm, ChangeAccountForm
from accounts.models import Customer

import json

import stripe

from zebra.forms import StripePaymentForm

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def profile(request):
    """
    Redirects to the user's profile.  To be used following login, so that
    we can redirect to whatever profile aspect we want.
    """
    return HttpResponseRedirect('/' + request.user.username + '/')

def logout_user(request):
    """
    Logs out the current user.
    """
    logout(request)
    return HttpResponseRedirect('/logout/success/')

def logout_and_view(request):
    """
    Logs out the current user and returns to their profile.
    """
    username = request.user.username
    logout(request)
    return HttpResponseRedirect('/' + username + '/')

def register_user(request, account_type):
    """
    Registers a new user to the site.  Works for free and paid
    accounts.
    """
    zebra_form_valid = True
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if account_type == settings.PREMIUM_ACCOUNT_NAME or account_type == settings.PROFESSIONAL_ACCOUNT_NAME:
            zebra_form = StripePaymentForm(request.POST)
            zebra_form_valid = zebra_form.is_valid()
        if user_form.is_valid() and zebra_form_valid:
            user = User.objects.create_user(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password1'],
                email=user_form.cleaned_data['email']
            )
            # Now, populate the profile from the form.
            profile = user.get_profile()
            # profile.field_1 = form.cleaned_data['field_1']
            profile.save()
            # Get the customer record that was automatically created
            customer = user.customer
            if account_type == settings.PROFESSIONAL_ACCOUNT_NAME:
                customer.account_limit = settings.PROFESSIONAL_IMAGE_LIMIT
            elif account_type == settings.PREMIUM_ACCOUNT_NAME:
                customer.account_limit = settings.PREMIUM_IMAGE_LIMIT
            else:
                customer.account_limit = settings.FREE_IMAGE_LIMIT
            # Accessing the stripe_customer attribute creates the stripe customer
            stripe_customer = customer.stripe_customer
            stripe_customer.email = user.email
            # Now, subscribe the (paying) customer to the appropriate plan
            if account_type != settings.FREE_ACCOUNT_NAME:
                stripe_customer.card = zebra_form.cleaned_data['stripe_token']
                stripe_customer.plan = account_type
            # Save both the model and the stripe customer
            customer.save()
            stripe_customer.save()
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])
            login(request, user)
            return HttpResponseRedirect('/accounts/profile/')
    else:
        user_form = RegistrationForm()
        if account_type == settings.PREMIUM_ACCOUNT_NAME or account_type == settings.PROFESSIONAL_ACCOUNT_NAME:
            zebra_form = StripePaymentForm()
        else:
            zebra_form = None
    variables = RequestContext(request, {'user_form': user_form, 'zebra_form': zebra_form, 'account_type': account_type})
    return render_to_response('registration/register.html', variables)

def delete_user(request):
    """
    Deletes the currently authenticated user's account and all associated data.
    """
    user = request.user
    if user and user.is_authenticated() and not user.is_staff:
        User.objects.get(username=user.username).delete()
    return HttpResponseRedirect('/')
        
def xhr_test(request):
    """
    Simple test view to try XHR GET and POST.
    """
    if request.is_ajax():
        if request.method == 'GET':
            message = 'This is an XHR GET request'
        elif request.method == 'POST':
            message = 'This is an XHR POST request'
            # can access the POST data here
            print request.POST
    else:
        message = 'This is not an XHR request'
    return HttpResponse(message)

def change_settings(request, username):
    """
    Allows the user to change their password and upgrade/downgrade account.
    """
    # Ensure that we cannot edit other user's profiles:
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    customer = request.user.customer
    if request.method == 'POST':
        change_account_form = ChangeAccountForm(request.POST)
        password_change_form = PasswordChangeForm(user=request.user, data=request.POST)
        if change_account_form.is_valid():
            customer.account_limit = change_account_form.cleaned_data['account_limit']
            customer.save()
            return HttpResponseRedirect('/' + username + '/')
        elif password_change_form.is_valid():
            password_change_form.save()
            return HttpResponseRedirect('/' + username + '/')
    else:
        change_account_form = ChangeAccountForm()
        password_change_form = PasswordChangeForm(user=request.user)
    profile = request.user.get_profile()
    variables = RequestContext(request,
                               {'username': username,
                                'customer': customer,
                                'profile': profile,
                                'change_account_form': change_account_form,
                                'password_change_form': password_change_form}
                               )
    return render_to_response('accounts/settings.html', variables)

def change_account(request, username):
    """
    Upgrade or downgrade the user's account.
    """
