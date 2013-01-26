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

    # Privacy policy.
    url(r'^privacy/$', direct_to_template, {'template': 'privacy.html'}),

    # Terms of use, including refund policy.
    url(r'^terms/$', direct_to_template, {'template': 'terms.html'}),

    # Password change form, redirects to login.
#    url(r'^password_change/$', 'django.contrib.auth.views.password_change',
#        {'post_change_redirect': '/login/'}),

    # Deletes the user's account.
    url(r'^delete/$', 'accounts.views.delete_user'),

    # Uncomment the next line to enable the admin:
    url(r'^spindrift/', include(admin.site.urls)),

    # Be sure to reserve all the above keywords by registering the following
    # users:
    # login, accounts, register, logout, welcome, password_change, delete,
    # privacy, terms, spindrift, admin

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

    # Deletes the gallery, and redirects back to the main portfolio.
    url(r'^(\w+)/gallery/(\d+)/delete/$', 'portfolios.views.delete_gallery'),

    # Deletes the profile photo, and redirects back to the profile (about page).
    url(r'^(\w+)/about/delete_photo/$', 'portfolios.views.delete_profile_photo'),

    # Allows the user to change their account settings.
    url(r'^(\w+)/settings/$', 'accounts.views.settings'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
