from rest_framework import serializers
from . import models


class OriginalUrlSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = models.OriginalUrl
        exclude = ['id']

    def get_user_id(self, obj):
        return obj.user_id.email


class ShortUrlSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    original_url = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    expires_at = serializers.DateTimeField(format="%Y-%m-%d %d %I:%M %p (UTC)", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %d %I:%M %p (UTC)", read_only=True)

    class Meta:
        model = models.ShortUrl
        fields = ['user_id', 'original_url', 'short_url', 'short_key', 'expires_at', 'created_at']

    def get_user_id(self, obj):
        return obj.user_id.email

    def get_original_url(self, obj):
        return obj.original_url_id.url

    def get_short_url(self, obj):
        return f"{self.context.get('request').build_absolute_uri('/')}r/{obj.short_key}/"


class ShortenUrlRequestSerializer(serializers.Serializer):
    url = serializers.URLField()
    expiry_date = serializers.DateField(required=False)
