from django.conf import settings

def domain(request):
    return {'DOMAIN': settings.DOMAIN}

def thumbnail_dimensions(request):
    return {'GALLERY_THUMBNAIL_DIMENSION': settings.GALLERY_THUMBNAIL_DIMENSION}
