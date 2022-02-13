from urllib.parse import urlparse
from django import forms
from service_objects.services import Service
from .models import PixelTracking


class TrackVisitor(Service):
    referer = forms.CharField(max_length=255)
    cookie = forms.CharField(max_length=255, required=False)

    def process(self):
        cookie = self.cleaned_data['cookie']

        path = urlparse(self.cleaned_data['referer']).path

        obj = PixelTracking(url=path)

        if cookie:
            obj.user_id = cookie

        obj.save()

        return obj.user_id
