from django.conf import settings

def domain(request):
    return {'DOMAIN': settings.DOMAIN}

def thumbnail_dimensions(request):
    return {'GALLERY_THUMBNAIL_DIMENSION': settings.GALLERY_THUMBNAIL_DIMENSION,
            'SQUARE_THUMBNAIL_DIMENSION': settings.SQUARE_THUMBNAIL_DIMENSION,
            'WIDE_THUMBNAIL_WIDTH': settings.WIDE_THUMBNAIL_WIDTH,
            'WIDE_THUMBNAIL_HEIGHT': settings.WIDE_THUMBNAIL_HEIGHT}
