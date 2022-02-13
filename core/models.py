import uuid
from django.db import models
from django.utils import timezone


class PixelTracking(models.Model):
    user_id = models.UUIDField(unique=False, default=uuid.uuid4)
    tracked_at = models.DateTimeField(
        max_length=30, db_index=True, default=timezone.now)
    url = models.URLField(max_length=30, db_index=True)
