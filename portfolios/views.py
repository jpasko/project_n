from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from accounts.forms import RegistrationForm
import json

def portfolio(request, username):
    """
    A user's portfolio.
    """
    user = get_object_or_404(User, username=username)
    fullname = user.get_profile().fullname
    variables = RequestContext(request, {'username': username, 'fullname': fullname})
    return render_to_response('portfolios/portfolio.html', variables)

def about(request, username):
    """
    A user's about page.
    """
    user = get_object_or_404(User, username=username)
    profile = user.get_profile()
    variables = RequestContext(request, {'username': username, 'profile': profile})
    return render_to_response('portfolios/about.html', variables)

def edit(request):
    """
    Allows a user to edit their profile.
    """

def upload(request):
    """
    Allows a user to upload a new photo.
    """

