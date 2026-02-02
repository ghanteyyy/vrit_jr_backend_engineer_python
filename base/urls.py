from . import views
from django.urls import path

urlpatterns = [
    path('', views.login_page),
    path('login/', views.login_page),
    path('register/', views.register_page),
    path('signup/', views.register_page),
    path('dashboard/', views.dashboard_page),
    path('r/<str:short_key>/', views.redirect_to_original),
    path('d/<str:short_key>/', views.view_details),
]
