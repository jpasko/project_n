from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import send_mail

from portfolios.models import Item, Photo, Video, Gallery
from portfolios.forms import *

from accounts.forms import ContactForm

import json

def portfolio(request):
    """
    A user's portfolio.
    """
    username = request.subdomain
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

def about(request):
    """
    A user's about page.
    """
    username = request.subdomain
    user = get_object_or_404(User, username=username)
    profile = user.get_profile()
    customer = user.customer
    variables = RequestContext(request,
                               {'username': username,
                                'customer': customer,
                                'profile': profile}
    )
    return render_to_response('portfolios/about.html', variables)

def edit(request):
    """
    Allows a user to edit their profile.
    """
    username = request.subdomain
    # Ensure that we cannot edit other user's profiles:
    if not username == request.user.username:
        raise Http404
    profile = request.user.get_profile()
    customer = request.user.customer
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/about/')
    else:
        form = UserProfileForm(instance=profile, initial={'allow_contact': profile.allow_contact})
    variables = RequestContext(request,
                               {'form': form,
                                'username': username,
                                'customer': customer,
                                'profile': profile})
    return render_to_response('portfolios/edit.html', variables)

def create_gallery(request):
    """
    Creates a new gallery.
    """
    username = request.subdomain
    # Ensure that we cannot create galleris on other portfolio:
    if not username == request.user.username:
        raise Http404
    if request.method == 'POST':
        form = CreateGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery = Gallery(
                user=request.user,
                title=form.cleaned_data['title'],
            )
            if request.FILES:
                gallery.thumbnail = form.cleaned_data['thumbnail']
            gallery.save()
            return HttpResponseRedirect('/')
    else:
        form = CreateGalleryForm()
    variables = RequestContext(request,
                               {'form': form,
                                'username': username,
                                'customer': request.user.customer,
                                'profile': request.user.get_profile()})
    return render_to_response('portfolios/create_gallery.html', variables)

def upload_image(request, gallery_id):
    """
    Allows a user to upload an image.
    """
    username = request.subdomain
    # Ensure that we cannot upload photos to another's portfolio:
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    profile = request.user.get_profile()
    customer = request.user.customer
    if request.method == 'POST':
        photo_form = UploadPhotoForm(request.POST, request.FILES)
        item_form = UploadItemForm(request.POST)
        if photo_form.is_valid() and item_form.is_valid():
            gallery = get_object_or_404(Gallery, pk=gallery_id)
            item = Item(
                gallery=gallery,
                caption=item_form.cleaned_data['caption'],
                is_photo=True
                )
            item.save()
            photo = Photo(
                item=item,
                image=request.FILES['image'],
                )
            photo.save()
            # Update the photo count on the user
            profile.photo_count += 1
            profile.save()
            # Update the photo count on the gallery
            gallery.count += 1
            gallery.save()
            return HttpResponseRedirect('/gallery/' + gallery_id + '/')
    else:
        item_form = UploadItemForm()
        photo_form = UploadPhotoForm()
    variables = RequestContext(request,
                               {'item_form': item_form,
                                'photo_form': photo_form,
                                'video_form': None,
                                'username': username,
                                'customer': customer,
                                'profile': profile})
    return render_to_response('portfolios/upload.html', variables)

def upload_video(request, gallery_id):
    """
    Allows a user to upload a new video.
    """
    username = request.subdomain
    # Ensure that we cannot upload photos to another's portfolio:
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    profile = request.user.get_profile()
    customer = request.user.customer
    if request.method == 'POST':
        video_form = UploadVideoForm(request.POST)
        if video_form.is_valid():
            gallery = get_object_or_404(Gallery, pk=gallery_id)
            item = Item(
                gallery=gallery,
                caption=video_form.cleaned_data['caption'],
                is_photo=False
                )
            item.save()
            video = Video(
                item=item,
                url=video_form.cleaned_data['url']
                )
            video.save()
            # Update the upload count on the user
            profile.photo_count += 1
            profile.save()
            # Update the count on the gallery
            gallery.count += 1
            gallery.save()
            return HttpResponseRedirect('/gallery/' + gallery_id + '/')
    else:
        video_form = UploadVideoForm()
    variables = RequestContext(request,
                               {'item_form': None,
                                'photo_form': None,
                                'video_form': video_form,
                                'username': username,
                                'customer': customer,
                                'profile': profile})
    return render_to_response('portfolios/upload.html', variables)

def gallery(request, gallery_id):
    """
    Gets all the items from a gallery.
    """
    username = request.subdomain
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

def delete_gallery(request, gallery_id):
    """
    Deletes the gallery (and all images it contains).
    """
    username = request.subdomain
    # First, check that the user is logged in and owns the gallery.
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    # Update the photo count on the user.
    profile = request.user.get_profile()
    profile.photo_count -= gallery.count
    if profile.photo_count < 0:
        profile.photo_count = 0
    profile.save()
    gallery.delete()
    return HttpResponseRedirect('/')

def delete_item(request, item_id):
    """
    Deletes the gallery item and decrements the gallery count.
    """
    username = request.subdomain
    # First, check that the user is logged in and owns the gallery.
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    item = get_object_or_404(Item, pk=item_id)
    gallery = item.gallery
    gallery.count -= 1
    gallery.save()
    item.delete()
    profile = request.user.get_profile()
    profile.photo_count -= 1
    if profile.photo_count < 0:
        profile.photo_count = 0
    profile.save()
    if gallery.count > 0:
        return HttpResponseRedirect('/gallery/' + str(gallery.pk) + '/')
    else:
        return HttpResponseRedirect('/')

def delete_profile_photo(request):
    """
    Deletes the profile photo.
    """
    username = request.subdomain
    # First, check that the user is logged in.
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    profile = request.user.get_profile()
    profile.picture = None
    profile.save()
    return HttpResponseRedirect('/about/')

def change_item_order(request):
    """
    Changes the order of items within a gallery.
    """
    results = {'success': False}
    if request.method == 'POST':
        if 'items[]' in request.POST:
            order = request.POST.getlist('items[]')
            for i in range(len(order)):
                item = get_object_or_404(Item, pk=order[i])
                item.order = i
                item.save()
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

def edit_item(request, item_id):
    """
    Allows the user to edit the item's caption.
    """
    username = request.subdomain
    # Ensure that we cannot edit another's photo:
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    profile = request.user.get_profile()
    customer = request.user.customer
    if request.method == 'POST':
        form = EditItemForm(request.POST)
        if form.is_valid():
            item = get_object_or_404(Item, pk=item_id)
            item.caption = form.cleaned_data['caption']
            item.save()
            gallery_id = item.gallery.pk
            return HttpResponseRedirect('/gallery/' + str(gallery_id) + '/')
    else:
        form = EditItemForm()
    variables = RequestContext(request,
                               {'form': form,
                                'username': username,
                                'customer': customer,
                                'profile': profile})
    return render_to_response('portfolios/edit_photo.html', variables)

def edit_gallery(request, gallery_id):
    """
    Allows the user to edit the gallery.
    """
    username = request.subdomain
    # Ensure that we cannot edit another's gallery:
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    profile = request.user.get_profile()
    customer = request.user.customer
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    if request.method == 'POST':
        form = EditGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery.title = form.cleaned_data['title']
            if request.FILES:
                gallery.thumbnail = request.FILES['thumbnail']
            else:
                gallery.thumbnail = None
            gallery.save()
            return HttpResponseRedirect('/')
    else:
        form = EditGalleryForm(initial = {'title': gallery.title,
                                          'thumbnail': gallery.thumbnail})
    variables = RequestContext(request,
                               {'form': form,
                                'username': username,
                                'customer': customer,
                                'profile': profile})
    return render_to_response('portfolios/edit_gallery.html', variables)

def contact(request):
    """
    Sends an email to the user when someone submits the form.
    """
    username = request.subdomain
    user = get_object_or_404(User, username=username)
    profile = user.get_profile()
    customer = user.customer
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            body = message
            if sender:
                body = body + '\n\nSender: ' + sender
            send_mail('Someone contacted you!', body, 'submissions@citreo.us', [user.email])
            variables = RequestContext(request,
                                       {'form': ContactForm(),
                                        'username': username,
                                        'profile': profile,
                                        'customer': customer,
                                        'thanks': True}
                                       )
            return render_to_response('portfolios/contact_page.html', variables)
    else:
        form = ContactForm()
    variables = RequestContext(request,
                              {'form': form,
                               'username': username,
                               'profile': profile,
                               'customer': customer,}
                               )
    return render_to_response('portfolios/contact_page.html', variables)

def toggle_contact(request):
    """
    Toggles the display of the contact page.
    """
    username = request.subdomain
    # Ensure that we cannot toggle the contact page of a different user.
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    profile = request.user.get_profile()
    results = {'success': False}
    if request.method == 'POST':
        if 'enable' in request.POST:
            enable = request.POST.get('enable') == 'True'
            profile.allow_contact = enable
            profile.save()
            results = {'success': True}
    return HttpResponse(json.dumps(results), mimetype='application/json')
