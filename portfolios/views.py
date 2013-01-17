from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from portfolios.models import Photo
from portfolios.forms import UserProfileForm, UploadPhotoForm
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
    variables = RequestContext(request,
                               {'username': username,
                                'profile': profile,
                                'fullname': profile.fullname}
    )
    return render_to_response('portfolios/about.html', variables)

def edit(request, username):
    """
    Allows a user to edit their profile.
    """
    # Ensure that we cannot edit other user's profiles:
    if not username == request.user.username:
        raise Http404
    profile = request.user.get_profile()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/' + username + '/about/')
    else:
        form = UserProfileForm(instance=profile)
    variables = RequestContext(request, {'form': form, 'username': username})
    return render_to_response('portfolios/edit.html', variables)

def upload(request, username):
    """
    Allows a user to upload a new photo.
    """
    if not username == request.user.username:
        raise Http404
    if request.method == 'POST':
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = Photo(
                user=request.user,
                image=request.FILES['image'],
                caption=form.cleaned_data['caption']
            )
            photo.save()
            return HttpResponseRedirect('/user/' + request.user.username + '/')
    else:
        form = UploadPhotoForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('portfolios/upload.html', variables)
