from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # The user's main profile, which shows their galleries.
    url(r'^$', 'portfolios.views.portfolio'),

    # A gallery.
    url(r'^gallery/(\d+)/$', 'portfolios.views.gallery'),

    # The about page of a user's profile.
    url(r'^about/$', 'portfolios.views.about'),

    # The contact page containing a contact form.
    url(r'^contact/$', 'portfolios.views.contact'),

    # A view handling ajax contact posts.
    url(r'^contact_ajax/$', 'portfolios.views.contact_ajax'),

    # Users can customize their portfolio.
    url(r'^customize/$', 'portfolios.views.customize'),

    # Users must create a gallery to upload photos into.
    url(r'^create_gallery/$', 'portfolios.views.create_gallery'),

    # Upload an image into the gallery.
    url(r'^upload/image/(\d+)/$', 'portfolios.views.upload_image'),

    # Upload a video into the gallery.
    url(r'^upload/video/(\d+)/$', 'portfolios.views.upload_video'),

    # Deletes the item, and redirects back to the gallery.  If
    # the gallery is empty, redirects back to the main profile.
    url(r'^item/(\d+)/delete/$', 'portfolios.views.delete_item'),

    # Edit an item's caption.
    url(r'^item/(\d+)/edit/$', 'portfolios.views.edit_item'),

    # Deletes a gallery, and redirect back to the main portfolio.
    url(r'^gallery/(\d+)/delete/$', 'portfolios.views.delete_gallery'),

    # Edit a gallery's title and thumbnail.
    url(r'^gallery/(\d+)/edit/$', 'portfolios.views.edit_gallery'),

    # Deletes the profile photo, and redirects back to the profile (about page).
    url(r'^about/delete_photo/$', 'portfolios.views.delete_profile_photo'),

    # Allows the user to change their account settings.
    url(r'^settings/$', 'accounts.views.change_settings'),

    # Change the credit card form.
    url(r'^accounts/change/$', 'accounts.views.change_credit_card'),

    # Account upgrade/downgrade page.  The view will handle free vs. paid users.
    url(r'^accounts/(\w+)/$', 'accounts.views.change_account'),

    # Add a credit card form.
    url(r'^accounts/(\w+)/payment/$', 'accounts.views.add_credit_card'),

    # Logs out the user, redirects to /logout/success/
    url(r'^logout/$', 'accounts.views.logout_user'),

    # Logs out the user, redirects to their portfolio
    url(r'^logout_view/$', 'accounts.views.logout_and_view'),

    # Reorder the galleries displayed on a user's profile.
    url(r'^reorder_galleries/$', 'portfolios.views.change_gallery_order'),

    # Reorder the items within a gallery.
    url(r'^reorder_items/$', 'portfolios.views.change_item_order'),

    # Deletes the user's account.
    url(r'^delete/$', 'accounts.views.delete_user'),

    # POST to this URL to toggle the display of the contact page.
    url(r'^toggle_contact_page/$', 'portfolios.views.toggle_contact'),

    # POST to this URL to toggle the display of the about page.
    url(r'^toggle_about_page/$', 'portfolios.views.toggle_about'),

    # POST to this URL to toggle the edit/view modes.
    url(r'^toggle_edit_mode/$', 'portfolios.views.toggle_edit_mode'),

    # POST here to disable the "Getting Started" modal on home view.
    url(r'^disable_get_started_modal/$', 'portfolios.views.disable_get_started_modal'),

    # POST to this URL to update the profile with AJAX.
    url(r'^update/$', 'portfolios.views.update_profile'),

    # POST to this URL to add/edit custom domain names.
    url(r'^custom_domain/$', 'portfolios.views.custom_domain'),

    # A help page.
    url(r'^help/$', 'portfolios.views.help'),

    # Edit the profile picture
    url(r'^edit_profile_picture/$', 'portfolios.views.edit_profile_picture'),

    # Robots.txt directly from template.
    url(r'^robots\.txt$', direct_to_template,
        {'template': 'robots.txt', 'mimetype': 'text/plain'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

if settings.DEV_SETTINGS:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
