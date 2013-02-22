from django.conf import settings
from django.core.urlresolvers import resolve
from django.http import HttpResponseRedirect

class SubdomainMiddleware:
    def process_request(self, request):
        """Parse out the subdomain from the request"""
        request.subdomain = None
        host = request.META.get('HTTP_HOST', '')
        host_s = host.replace('www.', '').split('.')
        if len(host_s) > 2:
            request.subdomain = ''.join(host_s[:-2])

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
        if subdomain != 'www' and subdomain is not None:
            # return HttpResponseRedirect("{0}://www.test.com:8000/{1}{2}".format(scheme, subdomain, path))
            request.subdomain = subdomain
            request.urlconf = settings.USER_URLS
        else:
            request.subdomain = None
            request.urlconf = settings.MAIN_URLS
