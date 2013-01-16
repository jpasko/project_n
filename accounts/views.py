from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from accounts.forms import RegistrationForm
import json

def about_user(request, username):
    """
    A user's profile and other information.
    """
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404('No account exists for user ' + username)
    # Get the profile, and render its contents with the template.
    profile = user.get_profile()
    variables = RequestContext(request, {
            'username': username, 'profile': profile})
    return render_to_response('accounts/about_user.html', variables)

@login_required
def profile(request):
    """
    Redirects to the user's profile.  To be used following login, so that
    we can redirect to whatever profile aspect we want.
    """
    return HttpResponseRedirect('/user/' + request.user.username + '/')

def logout_user(request):
    """
    Logs out the current user.
    """
    logout(request)
    return HttpResponseRedirect('/logout/success/')

def register_user(request, account_type):
    """
    Registers a new user to the site.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            # Now, populate the profile from the form.
            profile = user.get_profile()
            # profile.field_1 = form.cleaned_data['field_1']
            profile.save()
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])
            login(request, user)
            return HttpResponseRedirect('/accounts/profile/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form, 'account_type': account_type})
    return render_to_response('registration/register.html', variables)

def list_users(request):
    """
    Returns a list of all usernames.
    """
    all_users = User.objects.all()
    result = []
    if all_users.count() < 1:
        result.append('No users found')
    else:
        for user in all_users:
            result.append(user.username)
    # Convert the response to JSON.
    return HttpResponse(json.dumps(result))

def delete_user(request):
    """
    Deletes the currently authenticated user's account and all associated data.
    """
    user = request.user
    if user and user.is_authenticated() and not user.is_staff:
        User.objects.get(username=user.username).delete()
    return HttpResponseRedirect('/delete/success/')
        
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
