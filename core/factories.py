import factory
from faker import Faker
from django.utils import timezone
from . import models

Faker.seed('foo')
fake = Faker()


class PixelTrackingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PixelTracking

    url = '/contact.html'
    user_id = fake.uuid4()
    tracked_at = timezone.now()
