from django.test import TestCase, Client

from .models import PixelTracking


class TrackVisitorCase(TestCase):
    # def setUp(self):

    def test_first_call(self):
        client = Client(HTTP_REFERER='http://www.example.com/foo')
        res = client.get('/tracker')

        self.assertEqual(res.status_code, 200)

        uuid = res.cookies.get('tracker').value
        obj = PixelTracking.objects.first()

        self.assertEqual(str(obj.user_id), uuid)
        self.assertEqual(obj.url, '/foo')
        self.assertIsNotNone(obj.tracked_at)

    def test_multiple_calls(self):
        client = Client(HTTP_REFERER='http://www.example.com/foo')

        res = client.get('/tracker')
        self.assertEqual(res.status_code, 200)

        res = client.get('/tracker')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(PixelTracking.objects.count(), 2)

        first = PixelTracking.objects.first()
        last = PixelTracking.objects.last()
        self.assertEqual(first.user_id, last.user_id)

    def test_missing_referer(self):
        res = self.client.get('/tracker')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(PixelTracking.objects.count(), 0)

    def test_incorrect_tracker(self):
        client = Client(HTTP_REFERER='http://www.example.com/incorrect')
        client.cookies['tracker'] = 'invalid-uuid'
        res = client.get('/tracker')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(PixelTracking.objects.count(), 0)
