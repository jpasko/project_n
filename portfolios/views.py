from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import send_mail
from django.core.validators import validate_email, URLValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from portfolios.models import Item, Photo, Video, Gallery
from portfolios.forms import *

from accounts.forms import ContactForm
from accounts.models import Domains

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
    if not profile.allow_about:
        if username != request.user.username or not request.user.is_authenticated():
            raise Http404
    customer = user.customer
    variables = RequestContext(request,
                               {'username': username,
                                'customer': customer,
                                'profile': profile}
    )
    return render_to_response('portfolios/about.html', variables)

def customize(request):
    """
    Allows a user to customize their portfolio's style.
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
            return HttpResponseRedirect('/')
    else:
        form = UserProfileForm(instance=profile)
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
            return HttpResponseRedirect('/gallery/' + str(gallery.pk) + '/')
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
    error = None
    if request.method == 'POST':
        photo_form = UploadPhotoForm(request.POST, request.FILES)
        item_form = UploadItemForm(request.POST)
        if photo_form.is_valid() and item_form.is_valid():
            image=request.FILES['image']
            if image.size > settings.MAX_FILE_SIZE:
                error = 'Image too large!  Images must be less than 4 MB.'
            else:
                gallery = get_object_or_404(Gallery, pk=gallery_id)
                item = Item(
                    gallery=gallery,
                    caption=item_form.cleaned_data['caption'],
                    is_photo=True,
                    )
                item.save()
                photo = Photo(
                    item=item,
                    image=image,
                    )
                try:
                    photo.save()
                except Exception as e:
                    item.delete()
                    error = 'This image is corrupted!'
                else:
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
                                'gallery_id': gallery_id,
                                'username': username,
                                'error': error,
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
                                'gallery_id': gallery_id,
                                'username': username,
                                'error': None,
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
    return HttpResponseRedirect('/gallery/' + str(gallery.pk) + '/')

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
    item = get_object_or_404(Item, pk=item_id)
    profile = request.user.get_profile()
    customer = request.user.customer
    if request.method == 'POST':
        form = EditItemForm(request.POST)
        if form.is_valid():
            item.caption = form.cleaned_data['caption']
            item.save()
            gallery_id = item.gallery.pk
            return HttpResponseRedirect('/gallery/' + str(gallery_id) + '/')
    else:
        form = EditItemForm()
    variables = RequestContext(request,
                               {'form': form,
                                'item': item,
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
            elif form.cleaned_data['delete_current_thumbnail'] == 'True':
                gallery.thumbnail = None
            gallery.save()
            return HttpResponseRedirect('/gallery/' + str(gallery_id) + '/')
    else:
        form = EditGalleryForm()
    variables = RequestContext(request,
                               {'form': form,
                                'username': username,
                                'gallery': gallery,
                                'customer': customer,
                                'profile': profile})
    return render_to_response('portfolios/edit_gallery.html', variables)

@csrf_exempt
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
            send_mail('Someone contacted you!', body, 'submissions@folio24.com', [user.email])
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

@csrf_exempt
def contact_ajax(request):
    """
    Sends an email to the user when someone contacts them via ajax.
    """
    username = request.subdomain
    user = get_object_or_404(User, username=username)
    results = {'success': False}
    if request.method == 'POST':
        if 'message' in request.POST:
            message = request.POST.get('message')
            if message != '':
                body = message
                if 'name' in request.POST:
                    name = request.POST.get('name')
                    if name != '':
                        body = body + '\n\n-' + name
                if 'subject' in request.POST:
                    subject = request.POST.get('subject')
                    if subject != '':
                        body = 'Re: ' + subject + '\n\n' + body
                if 'sender' in request.POST:
                    sender = request.POST.get('sender')
                    if sender != '':
                        body = 'Email: ' + sender + '\n\n' + body
                send_mail('Someone contacted you!', body, 'submissions@folio24.com', [user.email])
                results = {'success': True}
    return HttpResponse(json.dumps(results), mimetype='application/json')

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

def toggle_about(request):
    """
    Toggles the display of the about page.
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
            profile.allow_about = enable
            profile.save()
            results = {'success': True}
    return HttpResponse(json.dumps(results), mimetype='application/json')

def update_profile(request):
    """
    Responds to AJAX POSTs to update the profile.
    """
    username = request.subdomain
    # Ensure that we cannot edit the profile of another user.
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    profile = request.user.get_profile()
    results = {'success': False,
               'message': ''}
    if request.method == 'POST':
        if 'about' in request.POST:
            profile.about = request.POST.get('about')
            profile.save()
            results['success'] = True
        elif 'email' in request.POST:
            email = request.POST.get('email')
            try:
                validate_email(email)
            except ValidationError:
                if email == '':
                    profile.email = ''
                    profile.save()
                    results['success'] = True
                else:
                    results['message'] = 'Invalid email address'
            else:
                profile.email = email
                profile.save()
                results['success'] = True
        elif 'phone' in request.POST:
            profile.phone = request.POST.get('phone')
            profile.save()
            results['success'] = True
        elif 'location' in request.POST:
            profile.location = request.POST.get('location')
            profile.save()
            results['success'] = True
        else:
            validate = URLValidator()
            if 'website' in request.POST:
                url = request.POST.get('website')
                try:
                    validate(url)
                except ValidationError:
                    if url == '':
                        profile.website = ''
                        profile.save()
                        results['success'] = True
                    else:
                        results['success'] = False
                        results['message'] = 'Invalid website URL.  Begin URL with \"http://\" or \"https://\".\n'
                else:
                    profile.website = url
                    profile.save()
                    results['success'] = True
            if 'blogger' in request.POST:
                url = request.POST.get('blogger')
                try:
                    validate(url)
                except ValidationError:
                    if url == '':
                        profile.blogger = ''
                        profile.save()
                        if not results['message']:
                            results ['success'] = True
                    else:
                        results['success'] = False
                        results['message'] = results['message'] + 'Invalid Blogger URL.  Begin URL with \"http://\" or \"https://\".\n'
                else:
                    profile.blogger = url
                    profile.save()
                    if not results['message']:
                        results ['success'] = True
            if 'deviantart' in request.POST:
                url = request.POST.get('deviantart')
                try:
                    validate(url)
                except ValidationError:
                    if url == '':
                        profile.deviantart = ''
                        profile.save()
                        if not results['message']:
                            results ['success'] = True
                    else:
                        results['success'] = False
                        results['message'] = results['message'] + 'Invalid deviantART URL.  Begin URL with \"http://\" or \"https://\".\n'
                else:
                    profile.deviantart = url
                    profile.save()
                    if not results['message']:
                        results ['success'] = True
            if 'digg' in request.POST:
                url = request.POST.get('digg')
                try:
                    validate(url)
                except ValidationError:
                    if url == '':
                        profile.digg = ''
                        profile.save()
                        if not results['message']:
                            results ['success'] = True
                    else:
                        results['success'] = False
                        results['message'] = results['message'] + 'Invalid Digg URL.  Begin URL with \"http://\" or \"https://\".\n'
                else:
                    profile.digg = url
                    profile.save()
                    if not results['message']:
                        results ['success'] = True
            if 'facebook' in request.POST:
                url = request.POST.get('facebook')
                try:
                    validate(url)
                except ValidationError:
                    if url == '':
                        profile.facebook = ''
                        profile.save()
                        if not results['message']:
                            results ['success'] = True
                    else:
                        results['success'] = False
                        results['message'] = results['message'] + 'Invalid Facebook URL.  Begin URL with \"http://\" or \"https://\".\n'
                else:
                    profile.facebook = url
                    profile.save()
                    if not results['message']:
                        results ['success'] = True
            if 'flickr' in request.POST:
                url = request.POST.get('flickr')
                try:
                    validate(url)
                except ValidationError:
                    if url == '':
                        profile.flickr = ''
                        profile.save()
                        if not results['message']:
                            results ['success'] = True
                    else:
                        results['success'] = False
                        results['message'] = results['message'] + 'Invalid Flickr URL.  Begin URL with \"http://\" or \"https://\".\n'
                else:
                    profile.flickr = url
                    profile.save()
                    if not results['message']:
                        results ['success'] = True
            if 'google_plus' in request.POST:
                url = request.POST.get('google_plus')
                try:
                    validate(url)
                except ValidationError:
                    if url == '':
                        profile.google_plus = ''
                        profile.save()
                        if not results['message']:
                            results ['success'] = True
                    else:
                        results['success'] = False
                        results['message'] = results['message'] + 'Invalid Google+ URL.  Begin URL with \"http://\" or \"https://\".\n'
                else:
                    profile.google_plus = url
                    profile.save()
                    if not results['message']:
                        results ['success'] = True
            if 'linkedin' in request.POST:
                url = request.POST.get('linkedin')
                try:
                    validate(url)
                except ValidationError:
                    if url == '':
                        profile.linkedin = ''
                        profile.save()
                        if not results['message']:
                            results ['success'] = True
                    else:
                        results['success'] = False
                        results['message'] = results['message'] + 'Invalid LinkedIn URL.  Begin URL with \"http://\" or \"https://\".'
                else:
                    profile.linkedin = url
                    profile.save()
                    if not results['message']:
                        results ['success'] = True
            if 'myspace' in request.POST:
                url = request.POST.get('myspace')
                try:
                    validate(url)
                except ValidationError:
                    if url == '':
                        profile.myspace = ''
                        profile.save()
                        if not results['message']:
                            results ['success'] = True
                    else:
                        results['success'] = False
                        results['message'] = results['message'] + 'Invalid Myspace URL.  Begin URL with \"http://\" or \"https://\".\n'
                else:
                    profile.myspace = url
                    profile.save()
                    if not results['message']:
                        results ['success'] = True
            if 'orkut' in request.POST:
                url = request.POST.get('orkut')
                try:
                    validate(url)
                except ValidationError:
                    if url == '':
                        profile.orkut = ''
                        profile.save()
                        if not results['message']:
                            results ['success'] = True
                    else:
                        results['success'] = False
                        results['message'] = results['message'] + 'Invalid Orkut URL.  Begin URL with \"http://\" or \"https://\".\n'
                else:
                    profile.orkut = url
                    profile.save()
                    if not results['message']:
                        results ['success'] = True
            if 'pinterest' in request.POST:
                url = request.POST.get('pinterest')
                try:
                    validate(url)
                except ValidationError:
                    if url == '':
                        profile.pinterest = ''
                        profile.save()
                        if not results['message']:
                            results ['success'] = True
                    else:
                        results['success'] = False
                        results['message'] = results['message'] + 'Invalid Pinterest URL.  Begin URL with \"http://\" or \"https://\".\n'
                else:
                    profile.pinterest = url
                    profile.save()
                    if not results['message']:
                        results ['success'] = True
            if 'tumblr' in request.POST:
                url = request.POST.get('tumblr')
                try:
                    validate(url)
                except ValidationError:
                    if url == '':
                        profile.tumblr = ''
                        profile.save()
                        if not results['message']:
                            results ['success'] = True
                    else:
                        results['success'] = False
                        results['message'] = results['message'] + 'Invalid Tumblr URL.  Begin URL with \"http://\" or \"https://\".\n'
                else:
                    profile.tumblr = url
                    profile.save()
                    if not results['message']:
                        results ['success'] = True
            if 'twitter' in request.POST:
                url = request.POST.get('twitter')
                try:
                    validate(url)
                except ValidationError:
                    if url == '':
                        profile.twitter = ''
                        profile.save()
                        if not results['message']:
                            results['success'] = True
                    else:
                        results['success'] = False
                        results['message'] = results['message'] + 'Invalid Twitter URL.  Begin URL with \"http://\" or \"https://\".\n'
                else:
                    profile.twitter = url
                    profile.save()
                    if not results['message']:
                        results['success'] = True
            if 'wordpress' in request.POST:
                url = request.POST.get('wordpress')
                try:
                    validate(url)
                except ValidationError:
                    if url == '':
                        profile.wordpress = ''
                        profile.save()
                        if not results['message']:
                            results ['success'] = True
                    else:
                        results['success'] = False
                        results['message'] = results['message'] + 'Invalid Wordpress URL.  Begin URL with \"http://\" or \"https://\".\n'
                else:
                    profile.wordpress = url
                    profile.save()
                    if not results['message']:
                        results ['success'] = True
            if 'youtube' in request.POST:
                url = request.POST.get('youtube')
                try:
                    validate(url)
                except ValidationError:
                    if url == '':
                        profile.youtube = ''
                        profile.save()
                        if not results['message']:
                            results ['success'] = True
                    else:
                        results['success'] = False
                        results['message'] = results['message'] + 'Invalid YouTube URL.  Begin URL with \"http://\" or \"https://\".\n'
                else:
                    profile.youtube = url
                    profile.save()
                    if not results['message']:
                        results ['success'] = True
    return HttpResponse(json.dumps(results), mimetype='application/json')

def help(request):
    """
    Simple help page for users to refer to.
    """
    username = request.subdomain
    # Ensure that the help page is only available to its owner.
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    profile = request.user.get_profile()
    customer = request.user.customer
    variables = RequestContext(request,
                              {'username': username,
                               'profile': profile,
                               'customer': customer,}
                               )
    return render_to_response('portfolios/help.html', variables)

def edit_profile_picture(request):
    """
    Allows the user to upload a new picture, or delete the current one.
    """
    username = request.subdomain
    # Ensure that we cannot toggle the contact page of a different user.
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    profile = request.user.get_profile()
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect('/about/')

def disable_get_started_modal(request):
    """
    Disables the display of the Getting Started modal.
    """
    username = request.subdomain
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    profile = request.user.get_profile()
    results = {'success': False}
    if request.method == 'POST':
        if 'disable' in request.POST:
            disable = request.POST.get('disable') == 'false'
            profile.show_get_started = disable
            profile.save()
            results = {'success': True}
    return HttpResponse(json.dumps(results), mimetype='application/json')

@csrf_exempt
def custom_domain(request):
    """
    Allows the user to enter a custom domain name.
    """
    username = request.subdomain
    user = request.user
    if username != user.username or not user.is_authenticated():
        raise Http404
    results = {'success': False}
    if request.method == 'POST':
        if 'domain' in request.POST:
            try:
                domain = Domains.objects.get(user=user)
            except Domains.DoesNotExist:
                new_domain = Domains(user=request.user, username=username, domain=request.POST.get('domain'))
                new_domain.save()
            else:
                domain.domain = request.POST.get('domain')
                domain.save()
            results = {'success': True}
    elif request.method == 'GET':
        try:
            domain = Domains.objects.get(user=user)
        except Domains.DoesNotExist:
            results = {'domain': ''}
        else:
            results = {'domain': domain.domain}
    return HttpResponse(json.dumps(results), mimetype='application/json')

@csrf_exempt
def toggle_edit_mode(request):
    """
    Toggles the edit/view modes.
    """
    username = request.subdomain
    if username != request.user.username or not request.user.is_authenticated():
        raise Http404
    profile = request.user.get_profile()
    results = {'success': False}
    if request.method == 'POST':
        if 'edit_mode' in request.POST:
            enable_edit_mode = request.POST.get('edit_mode') == 'True'
            profile.edit_mode = enable_edit_mode
            profile.save()
            results = {'success': True}
    return HttpResponse(json.dumps(results), mimetype='application/json')
