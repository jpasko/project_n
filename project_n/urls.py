from django.conf import settings
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

    # Logs out the user, redirects to their portfolio
    url(r'^logout_view/$', 'accounts.views.logout_and_view'),

    # Successful logout.
    url(r'^logout/success/$', direct_to_template,
        {'template': 'accounts/logout_success.html'}),

    # Page showing registration options.
    url(r'^register/$', direct_to_template,
        {'template': 'registration/registration_options.html'}),

    # User registration page.  The view will handle free vs. paid users.
    url(r'^register/(\w+)/$', 'accounts.views.register_user'),

    # Reorder the galleries displayed on a user's profile.
    url(r'^reorder_galleries/$', 'portfolios.views.change_gallery_order'),

    # Reorder the items within a gallery.
    url(r'^reorder_items/$', 'portfolios.views.change_item_order'),

    # Successful registration page, directs users to login and explains
    # what to do.
    url(r'^welcome/$', direct_to_template,
        {'template': 'accounts/welcome.html'}),

    # Privacy policy.
    url(r'^privacy/$', direct_to_template, {'template': 'privacy.html'}),

    # Terms of use, including refund policy.
    url(r'^terms/$', direct_to_template, {'template': 'terms.html'}),

    # About page.
    url(r'^about/$', direct_to_template, {'template': 'about_page.html'}),

    # Contact page.
    url(r'^contact/$', 'accounts.views.contact'),

    # Somewhat generic "thanks" page.
    url(r'^thanks/$', direct_to_template, {'template': 'thanks_page.html'}),

    # Password reset URLs.
    url(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/accounts/password/reset/done/'}),
    url(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/accounts/password/done/'}),
    url(r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete'),

    # Deletes the user's account.
    url(r'^delete/$', 'accounts.views.delete_user'),

    # Uncomment the next line to enable the admin:
    url(r'^spindrift/', include(admin.site.urls)),

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

    # Deletes the item, and redirects back to the gallery.  If
    # the gallery is empty, redirects back to the main profile.
    url(r'^(\w+)/item/(\d+)/delete/$', 'portfolios.views.delete_item'),

    # Edit an item's caption.
    url(r'^(\w+)/item/(\d+)/edit/$', 'portfolios.views.edit_item'),

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
