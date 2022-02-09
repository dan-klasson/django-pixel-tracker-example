from django.db import models


class PixelTracking(models.Model):
    user_id = models.UUIDField(unique=True)
    tracked_at = models.DateTimeField(max_length=30, db_index=True)
    url = models.URLField(max_length=30, db_index=True)
