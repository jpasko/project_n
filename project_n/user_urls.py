from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Logs out the user, redirects to /logout/success/
    url(r'^logout/$', 'accounts.views.logout_user'),

    # Logs out the user, redirects to their portfolio
    url(r'^logout_view/$', 'accounts.views.logout_and_view'),

    # Reorder the galleries displayed on a user's profile.
    url(r'^reorder_galleries/$', 'portfolios.views.change_gallery_order'),

    # Reorder the photos within a gallery.
    url(r'^reorder_photos/$', 'portfolios.views.change_photo_order'),

    # Password reset URLs.
    url(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/accounts/password/reset/done/'}),
    url(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/accounts/password/done/'}),
    url(r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete'),

    # Deletes the user's account.
    url(r'^delete/$', 'accounts.views.delete_user'),

    # Robots.txt directly from template.
    url(r'^robots\.txt$', direct_to_template,
        {'template': 'robots.txt', 'mimetype': 'text/plain'}),

    # The user's main profile, which shows their galleries.
    url(r'^(\w+)/$', 'portfolios.views.portfolio'),

    # A gallery.
    url(r'^(\w+)/gallery/(\d+)/$', 'portfolios.views.gallery'),

    # The about page of a user's profile.
    url(r'^(\w+)/about/$', 'portfolios.views.about'),

    # Users can edit their profile.
    url(r'^(\w+)/edit/$', 'portfolios.views.edit'),

    # Users must create a gallery to upload photos into.
    url(r'^(\w+)/create_gallery/$', 'portfolios.views.create_gallery'),

    # Users can upload new photos using the upload form.
    url(r'^(\w+)/upload/$', 'portfolios.views.upload'),

    # Users can upload photos directly to a gallery as well.
    url(r'^(\w+)/upload/(\d+)/$', 'portfolios.views.upload'),

    # Deletes the photo, and redirects back to the gallery.  If
    # the gallery is empty, redirects back to the main profile.
    url(r'^(\w+)/photo/(\d+)/delete/$', 'portfolios.views.delete_photo'),

    # Edit a photo's caption.
    url(r'^(\w+)/photo/(\d+)/edit/$', 'portfolios.views.edit_photo'),

    # Deletes a gallery, and redirect back to the main portfolio.
    url(r'^(\w+)/gallery/(\d+)/delete/$', 'portfolios.views.delete_gallery'),

    # Edit a gallery's title and thumbnail.
    url(r'^(\w+)/gallery/(\d+)/edit/$', 'portfolios.views.edit_gallery'),

    # Deletes the profile photo, and redirects back to the profile (about page).
    url(r'^(\w+)/about/delete_photo/$', 'portfolios.views.delete_profile_photo'),

    # Allows the user to change their account settings.
    url(r'^(\w+)/settings/$', 'accounts.views.change_settings'),

    # Change the credit card form.
    url(r'^(\w+)/accounts/change/$', 'accounts.views.change_credit_card'),

    # Account upgrade/downgrade page.  The view will handle free vs. paid users.
    url(r'^(\w+)/accounts/(\w+)/$', 'accounts.views.change_account'),

    # Add a credit card form.
    url(r'^(\w+)/accounts/(\w+)/payment/$', 'accounts.views.add_credit_card'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

if settings.DEV_SETTINGS:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
