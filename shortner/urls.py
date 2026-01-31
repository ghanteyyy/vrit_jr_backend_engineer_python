from . import views
from django.urls import path

urlpatterns = [
    path('api/url/shorten/', views.Shorten_URL.as_view(), name="shorten_url")
]

