from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail

from accounts.forms import RegistrationForm, ChangeAccountForm, ContactForm
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
    if account_type != settings.PROFESSIONAL_ACCOUNT_NAME and account_type != settings.PREMIUM_ACCOUNT_NAME and account_type != settings.FREE_ACCOUNT_NAME:
        raise Http404
    zebra_form_valid = True
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if account_type != settings.FREE_ACCOUNT_NAME:
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
            # Now, subscribe the customer to the appropriate stripe plan
            if account_type != settings.FREE_ACCOUNT_NAME:
                card = zebra_form.cleaned_data['stripe_token']
                stripe_customer.update_subscription(plan=account_type, card=card)
            else:
                stripe_customer.update_subscription(plan=account_type)
            # Save both the model and the stripe customer
            customer.save()
            stripe_customer.save()
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])
            login(request, user)
            return HttpResponseRedirect('/accounts/profile/')
    else:
        user_form = RegistrationForm()
        zebra_form = StripePaymentForm()
    # Make sure we don't pass a zebra form to the template if they're registering for a free account.
    if account_type == settings.FREE_ACCOUNT_NAME:
        zebra_form = None
    variables = RequestContext(request, {'user_form': user_form, 'zebra_form': zebra_form, 'account_type': account_type})
    return render_to_response('registration/register.html', variables)

def delete_user(request):
    """
    Deletes the currently authenticated user's account and all associated data.  Cancels their Stripe subscription, if
    it exists.
    """
    user = request.user
    if user and user.is_authenticated() and not user.is_staff:
        stripe_customer = stripe.Customer.retrieve(user.customer.stripe_customer_id)
        stripe_customer.cancel_subscription()
        stripe_customer.delete()
        User.objects.get(username=user.username).delete()
    return HttpResponseRedirect('/')

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

def change_account(request, username, new_account_type):
    """
    Upgrade or downgrade the user's account.
    """
    # Ensure that we cannot edit another user's account type:
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    user = request.user
    customer = user.customer
    stripe_customer = stripe.Customer.retrieve(customer.stripe_customer_id) 
    profile = user.get_profile()
    if new_account_type == settings.FREE_ACCOUNT_NAME:
        stripe_customer.update_subscription(plan=new_account_type, prorate=False)
        customer.account_limit = settings.FREE_IMAGE_LIMIT
        customer.save()
    elif new_account_type == settings.PREMIUM_ACCOUNT_NAME:
        if stripe_customer.active_card:
            stripe_customer.update_subscription(plan=new_account_type, prorate=False)
            customer.account_limit = settings.PREMIUM_IMAGE_LIMIT
            customer.save()
        else:
            return HttpResponseRedirect('/' + username + '/accounts/' + new_account_type + '/payment/')
    elif new_account_type == settings.PROFESSIONAL_ACCOUNT_NAME:
        if stripe_customer.active_card:
            stripe_customer.update_subscription(plan=new_account_type, prorate=False)
            customer.account_limit = settings.PROFESSIONAL_IMAGE_LIMIT
            customer.save()
        else:
            return HttpResponseRedirect('/' + username + '/accounts/' + new_account_type + '/payment/')
    else:
        raise Http404
    variables = RequestContext(request,
                               {'username': username,
                                'customer': customer,
                                'profile': profile,
                                'account_type': new_account_type}
                               )
    return render_to_response('accounts/change_account_success.html', variables)

def add_credit_card(request, username, account_type):
    """
    Adds a credit card and subscribes to the account type.
    """
    # Ensure that we cannot edit another user's account type:
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    if account_type != settings.PREMIUM_ACCOUNT_NAME and account_type != settings.PROFESSIONAL_ACCOUNT_NAME:
        raise Http404
    user = request.user
    customer = user.customer
    stripe_customer = stripe.Customer.retrieve(customer.stripe_customer_id)
    if stripe_customer.active_card:
        last_4 = stripe_customer.active_card.last4
    else:
        last_4 = None
    profile = user.get_profile()
    if request.method == 'POST':
        zebra_form = StripePaymentForm(request.POST)
        if zebra_form.is_valid():
            stripe_customer.card = zebra_form.cleaned_data['stripe_token']
            stripe_customer.save()
            stripe_customer.update_subscription(plan=account_type, prorate=False)
            if account_type == settings.PREMIUM_ACCOUNT_NAME:
                customer.account_limit = settings.PREMIUM_IMAGE_LIMIT
            else:
                customer.account_limit = settings.PROFESSIONAL_IMAGE_LIMIT
            customer.save()
            variables = RequestContext(request,
                                       {'username': username,
                                        'customer': customer,
                                        'profile': profile,
                                        'account_type': account_type}
                                       )
            return render_to_response('accounts/change_account_success.html', variables)
    else:
        zebra_form = StripePaymentForm()
    variables = RequestContext(request,
                               {'username': username,
                                'customer': customer,
                                'profile': profile,
                                'last_4': last_4,
                                'zebra_form': zebra_form}
                               )
    return render_to_response('accounts/credit_card_form.html', variables)
    
def change_credit_card(request, username):
    """
    Allows the user to update their credit card information
    """
    # Ensure that we cannot edit another user's account type:
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    user = request.user
    customer = user.customer
    stripe_customer = stripe.Customer.retrieve(customer.stripe_customer_id)
    if stripe_customer.active_card:
        last_4 = stripe_customer.active_card.last4
    else:
        last_4 = None
    profile = user.get_profile()
    if request.method == 'POST':
        zebra_form = StripePaymentForm(request.POST)
        if zebra_form.is_valid():
            stripe_customer.card = zebra_form.cleaned_data['stripe_token']
            stripe_customer.save()
            variables = RequestContext(request,
                                       {'username': username,
                                        'customer': customer,
                                        'profile': profile}
                                       )
            return render_to_response('accounts/update_card_success.html', variables)
    else:
        zebra_form = StripePaymentForm()
    variables = RequestContext(request,
                               {'username': username,
                                'customer': customer,
                                'profile': profile,
                                'last_4': last_4,
                                'zebra_form': zebra_form}
                               )
    return render_to_response('accounts/credit_card_form.html', variables)

def contact(request):
    """
    Sends an email to me when someone submits the contact form.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            body = 'Sender:\n' + sender + '\n\nMessage:\n' + message
            send_mail('Someone submitted the contact form', body, 'submissions@citreo.us', ['jbpasko@gmail.com'])
            return HttpResponseRedirect('/thanks/')

    else:
        form = ContactForm()
    variables = RequestContext(request,
                              {'form': form}
                              )
    return render_to_response('contact_page.html', variables)
