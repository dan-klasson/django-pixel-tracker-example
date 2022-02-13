from io import StringIO
from datetime import timedelta

from django.core.management import call_command
from django.utils import timezone
from django.test import TestCase

from core.factories import PixelTrackingFactory


class TrackerCommandTest(TestCase):
    def setUp(self):
        self.out = StringIO()

    def test_no_argument(self):
        PixelTrackingFactory.create_batch(5)
        PixelTrackingFactory(
            user_id='a6cb7db8-8af8-42aa-a30f-f2cd21370a24', url='/about.html')
        PixelTrackingFactory(
            user_id='b8dc5894-22ed-4f5b-b455-62ed1a8fab50', url='/about.html')

        call_command('tracker', stdout=self.out)

        self.assertIn(
            'contact.html\t\t| 5\t\t| 1',
            self.out.getvalue(),
        )
        self.assertIn(
            'about.html\t\t| 2\t\t| 2',
            self.out.getvalue(),
        )

    def test_from_argument(self):
        yesterday = timezone.now() - timedelta(days=1)
        one_min_past = timezone.now() - timedelta(minutes=1)
        date_time = one_min_past.strftime("%Y-%m-%d %H:%M:%S")

        PixelTrackingFactory(tracked_at=yesterday)
        PixelTrackingFactory()

        call_command('tracker', date_from=date_time, stdout=self.out)

        self.assertIn(
            'contact.html\t\t| 1\t\t| 1',
            self.out.getvalue(),
        )

    def test_to_argument(self):
        tomorrow = timezone.now() + timedelta(days=1)
        now_plus_seconds = timezone.now() + timedelta(seconds=60)
        date_time = now_plus_seconds.strftime("%Y-%m-%d %H:%M:%S")

        PixelTrackingFactory(tracked_at=tomorrow)
        PixelTrackingFactory()

        call_command('tracker', date_to=date_time, stdout=self.out)

        self.assertIn(
            'contact.html\t\t| 1\t\t| 1',
            self.out.getvalue(),
        )

    def test_both_arguments(self):
        yesterday = timezone.now() - timedelta(days=1)
        tomorrow = timezone.now() + timedelta(days=1)
        date_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

        PixelTrackingFactory(tracked_at=yesterday)
        now_plus_seconds = timezone.now() + timedelta(seconds=60)
        PixelTrackingFactory(tracked_at=now_plus_seconds)
        PixelTrackingFactory(tracked_at=tomorrow)

        call_command('tracker', date_to=date_time, stdout=self.out)

        self.assertIn(
            'contact.html\t\t| 1\t\t| 1',
            self.out.getvalue(),
        )

    def test_invalid_arguments(self):
        call_command('tracker', date_to='illegal', stdout=self.out)

        self.assertIn('Incorrect --date_to value', self.out.getvalue())

        call_command('tracker', date_from='illegal', stdout=self.out)

        self.assertIn('Incorrect --date_from value', self.out.getvalue())
