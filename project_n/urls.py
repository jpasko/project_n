from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # The main home page.  Rendered directly from a template.
    url(r'^$', direct_to_template,
        {'template': 'main_page.html'}),

    # The user's main profile, which shows their galleries.
    url(r'^user/(\w+)/$', 'portfolios.views.portfolio'),

    # A gallery.
    url(r'^user/(\w+)/gallery/(\d+)/$', 'portfolios.views.gallery'),

    # The about page of a user's profile.
    url(r'^user/(\w+)/about/$', 'portfolios.views.about'),

    # Users can edit their profile.
    url(r'^user/(\w+)/edit/$', 'portfolios.views.edit'),

    # Users must create a gallery to upload photos into.
    url(r'^user/(\w+)/create_gallery/$', 'portfolios.views.create_gallery'),

    # Users can upload new photos using the upload form.
    url(r'^user/(\w+)/upload/$', 'portfolios.views.upload'),

    # Deletes the photo, and redirects back to the gallery.
    # If the gallery is empty after deleting the photo, the gallery
    # is also deleted and they're redirected to the portfolio page.
#    url(r'^delete/photo/(\w+)/$', 'portfolios.views.delete_image'),

    # Deletes the gallery, and redirects back to the main profile.
    url(r'^user/(\w+)/gallery/(\d+)/delete/$', 'portfolios.views.delete_gallery'),

    # The login URL, should redirect to user/username/
    url(r'^login/$', 'django.contrib.auth.views.login'),

    # Here's the redirection from login
    url(r'^accounts/profile/$', 'accounts.views.profile'),

    # Logs out the user, redirects to /logout/success/
    url(r'^logout/$', 'accounts.views.logout_user'),

    # Successful logout.
    url(r'^logout/success/$', direct_to_template,
        {'template': 'accounts/logout_success.html'}),

    # Page showing registration options.
    url(r'^register/$', direct_to_template,
        {'template': 'registration/registration_options.html'}),

    # Different registration forms for free vs paid accounts.
    url(r'^register/(\w+)/$', 'accounts.views.register_user'),

    # Successful registration page, directs users to login and explains
    # what to do.
    url(r'^welcome/$', direct_to_template,
        {'template': 'accounts/welcome.html'}),

    # Password change form, redirects to success page.
#    url(r'^password_change/$', 'django.contrib.auth.views.password_change',
#        {'post_change_redirect': '/password_change/success/'}),

    # Success page for password change.
#    url(r'^password_change/success/$', direct_to_template,
#        {'template': 'registration/password_change_success.html'}),

    # Example portfolios, hand-curated.
#    url(r'^examples/$', direct_to_template,
#        {'template': 'direct/examples.html'}),

    # Confirmation of delete request.
#    url(r'^delete/confirm/$', direct_to_template,
#        {'template': 'direct/confirm_delete.html'}),

    # Deletes the user's account.
#    url(r'^delete/$', 'accounts.views.delete'),

    # Successful deletion of a user.
#    url(r'^delete/success/$', direct_to_template,
#        {'template': 'direct/user_delete_success.html'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^spindrift/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
