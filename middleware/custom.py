from django.conf import settings
from django.core.urlresolvers import resolve
from django.http import HttpResponseRedirect

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
