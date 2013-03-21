from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail

from accounts.forms import RegistrationForm, ChangeAccountForm, ContactForm, CardForm
from accounts.models import Customer, Domains

import json

import stripe

import datetime

from zebra.forms import StripePaymentForm

stripe.api_key = settings.STRIPE_SECRET

def soon():
    soon = datetime.date.today() + datetime.timedelta(days=30)
    return {'month': soon.month, 'year': soon.year}

def save_stripe_customer(stripe_customer):
    """
    Saves the stripe customer mit dem error-handling.  Returns
    None on success, and an error message to display to the user
    if the save failed.  Also sends me an email when the shit
    hits the fan.
    """
    message = None
    try:
        stripe_customer.save()
    except stripe.CardError as e:
        # Since it's a decline, stripe.CardError will be caught
        body = e.json_body
        err  = body['error']
        code = err['code']
        if err['message']:
            message = err['message']
        else:
            message = "An error occurred while processing your card"
        # details = "Status: %s\nType: %s\nCode: %s\nParam: %s\nMessage: %s\n" % (e.http_status, err['type'], err['code'], err['param'], err['message'])
        # send_mail('Card Error', details, 'errors@citreo.us', ['jbpasko@gmail.com'])
    except stripe.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        message = "We're having trouble processing your card.  Please try again."
        # send_mail('Invalid Request Error', 'Check the API call', 'errors@citreo.us', ['jbpasko@gmail.com'])
    except stripe.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        message = "We're having trouble processing your card.  Please try again."
        # send_mail('Authentication Error', 'Make sure the API keys are correct', 'errors@citreo.us', ['jbpasko@gmail.com'])
    except stripe.APIConnectionError as e:
        # Network communication with Stripe failed
        message = "We're having trouble processing your card.  Please try again."
        # send_mail('API Connection Error', 'Check the logs', 'errors@citreo.us', ['jbpasko@gmail.com'])
    except stripe.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        message = "We're having trouble processing your card.  Please try again."
        # send_mail('Stripe Error', 'Check the logs', 'errors@citreo.us', ['jbpasko@gmail.com'])
    except e:
        # Something else happened, completely unrelated to Stripe
        message = "An unexpected error occured while processing your card.  Please try again."
        # send_mail('Unknown Error', 'Check the logs', 'errors@citreo.us', ['jbpasko@gmail.com'])
    return message

@login_required
def profile(request):
    """
    Redirects to the user's profile.  To be used following login, so that
    we can redirect to whatever profile aspect we want.
    """
    return HttpResponseRedirect("http://{0}.{1}".format(request.user.username, settings.DOMAIN))


def logout_user(request):
    """
    Logs out the current user.
    """
    logout(request)
    return HttpResponseRedirect("http://www.{0}/logout/success".format(settings.DOMAIN))

def logout_and_view(request):
    """
    Logs out the current user and returns to their profile.
    """
    username = request.user.username
    logout(request)
    return HttpResponseRedirect('/')

def register_user(request, account_type):
    """
    Registers a new user to the site.  Works for free and paid
    accounts.
    """
    if account_type != settings.PROFESSIONAL_ACCOUNT_NAME and account_type != settings.PREMIUM_ACCOUNT_NAME and account_type != settings.FREE_ACCOUNT_NAME:
        raise Http404
    card_form_valid = True
    error = None
    paid = (account_type != settings.FREE_ACCOUNT_NAME)
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if account_type != settings.FREE_ACCOUNT_NAME:
            card_form = CardForm(request.POST)
            card_form_valid = card_form.is_valid()
        if user_form.is_valid() and card_form_valid:
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
            if account_type != settings.FREE_ACCOUNT_NAME:
                stripe_customer.card = card_form.cleaned_data['stripe_token']
            # If there's an error with the credit card, delete everything
            # and display the error message on the form.  Clearly a hacky way
            # to do this, and something I'll clean up later.
            error = save_stripe_customer(stripe_customer)
            if error is None:
                stripe_customer.update_subscription(plan=account_type)
                customer.save()
                user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
                login(request, user)
                return HttpResponseRedirect('/accounts/profile/')
            else:
                stripe_customer.delete()
                user.delete()
    else:
        user_form = RegistrationForm()
    now = datetime.datetime.now()
    variables = RequestContext(request,
                               {'user_form': user_form,
                                'publishable': settings.STRIPE_PUBLISHABLE,
                                'soon': soon(),
                                'months': range(1, 13),
                                'years': range(now.year, (now.year + 15)),
                                'error': error,
                                'account_type': account_type,
                                'paid': paid}
                               )
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
    return HttpResponseRedirect("http://www.{0}/".format(settings.DOMAIN))

def change_settings(request):
    """
    Allows the user to change their password and upgrade/downgrade account.
    """
    username = request.subdomain
    # Ensure that we cannot edit other user's profiles:
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    customer = request.user.customer
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            return HttpResponseRedirect("http://{0}.{1}".format(request.user.username, settings.DOMAIN))
    else:
        password_change_form = PasswordChangeForm(user=request.user)
    profile = request.user.get_profile()
    variables = RequestContext(request,
                               {'username': username,
                                'customer': customer,
                                'profile': profile,
                                'password_change_form': password_change_form}
                               )
    return render_to_response('accounts/settings.html', variables)

def change_account(request, new_account_type):
    """
    Upgrade or downgrade the user's account.
    """
    username = request.subdomain
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
        # Delete the domain name record.
        try:
            domain = Domains.objects.get(user=user)
        except Domains.DoesNotExist:
            pass
        else:
            domain.delete()
    elif new_account_type == settings.PREMIUM_ACCOUNT_NAME:
        if stripe_customer.active_card:
            stripe_customer.update_subscription(plan=new_account_type, prorate=False)
            customer.account_limit = settings.PREMIUM_IMAGE_LIMIT
            customer.save()
        else:
            return HttpResponseRedirect("https://{0}.{1}/accounts/{2}/payment/".format(request.user.username, settings.DOMAIN, new_account_type))
    elif new_account_type == settings.PROFESSIONAL_ACCOUNT_NAME:
        if stripe_customer.active_card:
            stripe_customer.update_subscription(plan=new_account_type, prorate=False)
            customer.account_limit = settings.PROFESSIONAL_IMAGE_LIMIT
            customer.save()
        else:
            return HttpResponseRedirect("https://{0}.{1}/accounts/{2}/payment/".format(request.user.username, settings.DOMAIN, new_account_type))
    else:
        raise Http404
    variables = RequestContext(request,
                               {'username': username,
                                'customer': customer,
                                'profile': profile,
                                'account_type': new_account_type}
                               )
    return render_to_response('accounts/change_account_success.html', variables)

def add_credit_card(request, account_type):
    """
    Adds a credit card and subscribes to the account type.
    """
    username = request.subdomain
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
    error = None
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            stripe_customer.card = form.cleaned_data['stripe_token']
            error = save_stripe_customer(stripe_customer)
            if error is None:
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
        form = CardForm()
    now = datetime.datetime.now()
    variables = RequestContext(request,
                               {'publishable': settings.STRIPE_PUBLISHABLE,
                                'soon': soon(),
                                'months': range(1, 13),
                                'years': range(now.year, (now.year + 15)),
                                'username': username,
                                'customer': customer,
                                'profile': profile,
                                'last_4': last_4,
                                'error': error}
                               )
    return render_to_response('accounts/credit_card_form.html', variables)
    
def change_credit_card(request):
    """
    Allows the user to update their credit card information
    """
    username = request.subdomain
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
    error = None
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            stripe_customer.card = form.cleaned_data['stripe_token']
            error = save_stripe_customer(stripe_customer)
            if error is None:
                variables = RequestContext(request,
                                           {'username': username,
                                            'customer': customer,
                                            'profile': profile}
                                           )
                return render_to_response('accounts/update_card_success.html', variables)
    else:
        form = CardForm()
    now = datetime.datetime.now()
    variables = RequestContext(request,
                               {'publishable': settings.STRIPE_PUBLISHABLE,
                                'soon': soon(),
                                'months': range(1, 13),
                                'years': range(now.year, (now.year + 15)),
                                'username': username,
                                'customer': customer,
                                'profile': profile,
                                'last_4': last_4,
                                'error': error}
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
            body = 'Sender: ' + sender + '\n\nMessage:\n' + message
            send_mail('Someone submitted the contact form', body, 'submissions@folio24.com', ['jbpasko@gmail.com'])
            return HttpResponseRedirect('/thanks/')

    else:
        form = ContactForm()
    variables = RequestContext(request,
                              {'form': form}
                              )
    return render_to_response('contact_page.html', variables)
