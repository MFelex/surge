from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('main.urls'), name='main'),
]
