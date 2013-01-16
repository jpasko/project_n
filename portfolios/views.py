from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from accounts.forms import RegistrationForm
import json

def portfolio(request, username):
    """
    A user's portfolio.
    """
    variables = RequestContext(request, {'username': username})
    return render_to_response('portfolios/portfolio.html', variables)
