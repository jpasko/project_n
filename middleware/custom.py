from django.conf import settings
from django.core.urlresolvers import resolve
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from accounts.models import Domains

class SubdomainURLs:
    """
    Sets the subdomain and urlconf attribute on the request context.
    """

    def process_request(self, request):
        scheme = "http" if not request.is_secure() else "https"
        path = request.get_full_path()
        domain = request.META.get('HTTP_HOST') or request.META.get('SERVER_NAME')
        pieces = domain.split('.')
        subdomain = ".".join(pieces[:-2])
        if subdomain != 'www' and subdomain != '' and subdomain is not None:
            request.subdomain = subdomain
            request.urlconf = settings.USER_URLS
        else:
            request.subdomain = None
            request.urlconf = settings.MAIN_URLS

class ParseURLs:
    """
    Sets the subdomain and urlconf attribute on the request context.
    """

    def process_request(self, request):
        domain = request.get_host()
        pieces = domain.split('.')
        subdomain = ".".join(pieces[:-2])
        root = ".".join(pieces[-2:])
        if root != settings.DOMAIN:
            # Look up the user associated with this domain, and hijack the
            # subdomain attribute of the request.  Poorly named, I know...
            user_domain = get_object_or_404(Domains, domain=root)
            request.subdomain = user_domain.user.username
            request.urlconf = settings.USER_URLS
        elif subdomain != 'www' and subdomain != '' and subdomain is not None:
            request.subdomain = subdomain
            request.urlconf = settings.USER_URLS
        else:
            request.subdomain = None
            request.urlconf = settings.MAIN_URLS
