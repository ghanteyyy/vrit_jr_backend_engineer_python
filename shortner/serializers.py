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

    class Meta:
        model = models.ShortUrl
        fields = ['user_id', 'original_url', 'short_url']

    def get_user_id(self, obj):
        return obj.user_id.email

    def get_original_url(self, obj):
        return obj.original_url_id.url

    def get_short_url(self, obj):
        return f"{self.context.get('request').build_absolute_uri('/')}{obj.short_key}"
