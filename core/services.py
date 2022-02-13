from urllib.parse import urlparse
from django.core.management.base import CommandError
from datetime import datetime
from django.db.models import Count
from django.utils.timezone import make_aware
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


class TrackerCommand(Service):
    date_from = forms.CharField(required=False)
    date_to = forms.CharField(required=False)

    def process(self):
        filters = {}
        date_from = self.cleaned_data['date_from']
        date_to = self.cleaned_data['date_to']

        if date_from:
            try:
                filters['tracked_at__gte'] = make_aware(datetime.strptime(
                    date_from, "%Y-%m-%d %H:%M:%S"))
            except ValueError:
                raise CommandError('Incorrect --date_from value')

        if date_to:
            try:
                filters['tracked_at__lte'] = make_aware(datetime.strptime(
                    date_to, "%Y-%m-%d %H:%M:%S"))
            except ValueError:
                raise CommandError('Incorrect --date_to value')

        return PixelTracking.objects \
            .values('url') \
            .annotate(page_views=Count('url')) \
            .annotate(visitors=Count('user_id', distinct=True)) \
            .filter(**filters)
