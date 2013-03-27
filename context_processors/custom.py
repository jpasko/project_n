from django.conf import settings

def domain(request):
    return {'DOMAIN': settings.DOMAIN}

def sizes_and_dimensions(request):
    return {'GALLERY_THUMBNAIL_DIMENSION': settings.GALLERY_THUMBNAIL_DIMENSION,
            'MAX_FILE_SIZE': settings.MAX_FILE_SIZE}
