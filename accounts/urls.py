from . import views
from django.urls import path

urlpatterns = [
    path('api/auth/login/', views.Login),
    path('api/auth/register/', views.Register),
    path('api/auth/logout/', views.Logout),
]

