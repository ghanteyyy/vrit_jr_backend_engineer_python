from datetime import timedelta
from django.db import models
from django.utils import timezone
from utils import utils


def expires_at():
    return timezone.now() + timedelta(hours=24)


class OriginalUrl(models.Model):
    id = models.CharField(primary_key=True, default=utils.generate_uuid_hex, max_length=255)
    user_id = models.ForeignKey(to="accounts.CustomUser", on_delete=models.CASCADE)

    url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class ShortUrl(models.Model):
    id = models.CharField(primary_key=True, default=utils.generate_uuid_hex, max_length=255)
    user_id = models.ForeignKey(to="accounts.CustomUser", on_delete=models.CASCADE)
    original_url_id = models.ForeignKey(OriginalUrl, on_delete=models.CASCADE)

    short_key = models.CharField(blank=False, null=False, max_length=10, default=utils.generate_short_key)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=expires_at)
