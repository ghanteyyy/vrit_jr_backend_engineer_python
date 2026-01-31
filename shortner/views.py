from django.utils import timezone
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view, APIView
from . import models
from . import serializers


class Shorten_URL(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        short_urls = models.ShortUrl.objects.filter(user_id=request.user)

        # Delete all expired links
        for short_url in short_urls[:]:
            if timezone.now() >= short_url.expires_at:
                short_url.original_url_id.delete()
                short_urls.remove(short_url)

        return Response({
            "status": True,
            "details": serializers.ShortUrlSerializer(short_urls, many=True, context={"request": request}).data
        })

    def post(self, request):
        self.get(request)     # Removing expired links (if any). In future, use celery as background scheduler.

        url = request.data.get("url")

        if models.OriginalUrl.objects.filter(url__iexact=url).exists():
            short_url = models.ShortUrl.objects.get(original_url_id__url__iexact=url)

            return Response({
                "status": True,
                "details": serializers.ShortUrlSerializer(short_url, context={"request": request}).data
            })

        original_url = models.OriginalUrl(user_id=request.user, url=url)
        original_url.save()

        short_url = models.ShortUrl(user_id=request.user, original_url_id=original_url)
        short_url.save()

        return Response({
            "status": True,
            "details": serializers.ShortUrlSerializer(short_url, context={"request": request}).data
        })
