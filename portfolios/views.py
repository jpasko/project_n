from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from portfolios.models import Photo, Gallery
from portfolios.forms import *

import json

def portfolio(request, username):
    """
    A user's portfolio.
    """
    user = get_object_or_404(User, username=username)
    # Retrieve all galleries, including empty ones, iff the user is logged in
    if request.user.is_authenticated() and request.user.username == username:
        galleries = user.gallery_set.all()
    else:
        # Only show non-empty galleries to a guest.
        galleries = user.gallery_set.filter(count__gt=0)
    profile = user.get_profile()
    customer = user.customer
    variables = RequestContext(request, {
            'username': username,
            'profile': profile,
            'customer': customer,
            'galleries': galleries})
    return render_to_response('portfolios/portfolio.html', variables)

def about(request, username):
    """
    A user's about page.
    """
    user = get_object_or_404(User, username=username)
    profile = user.get_profile()
    customer = user.customer
    variables = RequestContext(request,
                               {'username': username,
                                'customer': customer,
                                'profile': profile}
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
    customer = request.user.customer
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/' + username + '/about/')
    else:
        form = UserProfileForm(instance=profile)
    variables = RequestContext(request,
                               {'form': form,
                                'username': username,
                                'customer': customer,
                                'profile': profile})
    return render_to_response('portfolios/edit.html', variables)

def create_gallery(request, username):
    """
    Creates a new gallery.
    """
    # Ensure that we cannot create galleris on other portfolio:
    if not username == request.user.username:
        raise Http404
    if request.method == 'POST':
        form = CreateGalleryForm(request.POST)
        if form.is_valid():
            gallery = Gallery(
                user=request.user,
                title=form.cleaned_data['title'],
            )
            gallery.save()
            return HttpResponseRedirect('/' + username + '/')
    else:
        form = CreateGalleryForm()
    variables = RequestContext(request,
                               {'form': form,
                                'username': username,
                                'customer': request.user.customer,
                                'profile': request.user.get_profile()})
    return render_to_response('portfolios/create_gallery.html', variables)

def upload(request, username, gallery_id=None):
    """
    Allows a user to upload a new photo.
    """
    # Ensure that we cannot upload photos to another's portfolio:
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    profile = request.user.get_profile()
    customer = request.user.customer
    if request.method == 'POST':
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            gallery = form.cleaned_data['gallery']
            photo = Photo(
                gallery=gallery,
                image=request.FILES['image'],
                caption=form.cleaned_data['caption']
            )
            photo.save()
            # Update the photo count on the user
            profile.photo_count += 1
            profile.save()
            # Update the photo count on the gallery
            gallery.count += 1
            gallery.save()
            return HttpResponseRedirect('/' + username + '/')
    elif gallery_id:
        form = UploadPhotoForm(initial = {'gallery': get_object_or_404(Gallery, pk=gallery_id)})
    else:
        form = UploadPhotoForm()
    variables = RequestContext(request,
                               {'form': form,
                                'username': username,
                                'customer': customer,
                                'profile': profile})
    return render_to_response('portfolios/upload.html', variables)

def gallery(request, username, gallery_id):
    """
    Gets all the photos from a gallery.
    """
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    user = get_object_or_404(User, username=username)
    profile = user.get_profile()
    customer = user.customer
    variables = RequestContext(request, {
            'gallery': gallery,
            'profile': profile,
            'customer': customer,
            'username': username})
    return render_to_response('portfolios/gallery.html', variables)

def delete_gallery(request, username, gallery_id):
    """
    Deletes the gallery (and all images it contains).
    """
    # First, check that the user is logged in and owns the gallery.
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    # Update the photo count on the user.
    profile = request.user.get_profile()
    profile.photo_count -= gallery.count
    profile.save()
    gallery.delete()
    return HttpResponseRedirect('/' + username + '/')

def delete_photo(request, username, photo_id):
    """
    Deletes the image and decrements the gallery count.
    """
    # First, check that the user is logged in and owns the gallery.
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    photo = get_object_or_404(Photo, pk=photo_id)
    gallery = photo.gallery
    gallery.count -= 1
    gallery.save()
    photo.delete()
    profile = request.user.get_profile()
    profile.photo_count -= 1
    profile.save()
    redirect_url = '/' + username + '/'
    if gallery.count > 0:
        return HttpResponseRedirect(redirect_url + 'gallery/' + str(gallery.pk) + '/')
    else:
        return HttpResponseRedirect(redirect_url)

def delete_profile_photo(request, username):
    """
    Deletes the profile photo.
    """
    # First, check that the user is logged in.
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    profile = request.user.get_profile()
    profile.picture = None
    profile.save()
    return HttpResponseRedirect('/' + username + '/about/')

def change_photo_order(request):
    """
    Changes the order of photos within a gallery.
    """
    results = {'success': False}
    if request.method == 'POST':
        if 'photos[]' in request.POST:
            order = request.POST.getlist('photos[]')
            for i in range(len(order)):
                photo = get_object_or_404(Photo, pk=order[i])
                photo.order = i
                photo.save()
            results = {'success': True}
    return HttpResponse(json.dumps(results), mimetype='application/json')

def change_gallery_order(request):
    """
    Changes the order of galleries within the portfolio.
    """
    results = {'success': False}
    if request.method == 'POST':
        if 'galleries[]' in request.POST:
            order = request.POST.getlist('galleries[]')
            for i in range(len(order)):
                gallery = get_object_or_404(Gallery, pk=order[i])
                gallery.order = i
                gallery.save()
            results = {'success': True}
    return HttpResponse(json.dumps(results), mimetype='application/json')

def edit_photo_caption(request):
    """
    Allows the user to edit the photo's caption.
    """

def edit_gallery_title(request):
    """
    Allows the user to edit the gallery's title.
    """
