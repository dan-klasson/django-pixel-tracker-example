import base64
from urllib.parse import urlparse
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse, parse_cookie
from django.core.exceptions import SuspiciousOperation, ValidationError


from .services import TrackVisitor


def track_visitor(request):
    b64 = b"R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    PIXEL_GIF_DATA = base64.b64decode(b64)

    cookies = parse_cookie(request.META.get('HTTP_COOKIE'))

    try:
        user_id = TrackVisitor.execute({
            'cookie': cookies.get('tracker'),
            'referer': request.META.get('HTTP_REFERER')
        })
    except:
        # would log this
        raise SuspiciousOperation()

    response = HttpResponse(PIXEL_GIF_DATA, content_type='image/gif')

    if 'tracker' not in cookies:
        response.set_cookie('tracker', user_id)

    return response
