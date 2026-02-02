import datetime
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from rest_framework.decorators import APIView
from . import models
from . import serializers


class Shorten_URL(APIView):
    permission_classes = [IsAuthenticated]

    def get_valid_links(self, request):
        '''
        Return links that are not expired
        '''

        short_urls = models.ShortUrl.objects.filter(user_id=request.user)

        for short_url in short_urls[:]:
            if timezone.now() >= short_url.expires_at:
                short_url.original_url_id.delete()
                short_urls.remove(short_url)

        return short_urls

    def get(self, request):
        short_urls = self.get_valid_links(request)

        return Response({
            "status": True,
            "details": serializers.ShortUrlSerializer(short_urls, many=True, context={"request": request}).data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        self.get_valid_links(request)     # Removing expired links (if any). In future, use celery as background scheduler.

        url = request.data.get("url")
        expiry_date = request.data.get("expiry_date")

        if models.OriginalUrl.objects.filter(url__iexact=url).exists():
            short_url = models.ShortUrl.objects.get(original_url_id__url__iexact=url)

            return Response({
                "status": True,
                "details": serializers.ShortUrlSerializer(short_url, context={"request": request}).data
            }, status=status.HTTP_200_OK)

        original_url = models.OriginalUrl(user_id=request.user, url=url)
        original_url.save()

        expiry_date = datetime.datetime.strptime(expiry_date, "%Y-%m-%d")

        short_url = models.ShortUrl(user_id=request.user, original_url_id=original_url, expires_at=expiry_date)
        short_url.save()

        return Response({
            "status": True,
            "details": serializers.ShortUrlSerializer(short_url, context={"request": request}).data
        }, status=status.HTTP_201_CREATED)

    def delete(self, request):
        short_key = request.data.get('short_key')

        try:
            original = models.ShortUrl.objects.get(user_id=request.user, short_key=short_key).original_url_id
            original.delete()

            return Response({
                "status": True,
                "message": "Delete successful"
            }, status=status.HTTP_200_OK)

        except models.ShortUrl.DoesNotExist:
            return Response({
                "status": False,
                "message": "Provided link does not exist"
            }, status=status.HTTP_404_NOT_FOUND)
