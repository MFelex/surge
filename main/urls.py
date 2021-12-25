from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path
from main.views import (
    FactorView,
    RegisterView,
    SurgeDurationView,
    ThresholdCoefficientView,
)


urlpatterns = [
    path('user/register', RegisterView.as_view(), name='register'),
    path('user/login', TokenObtainPairView.as_view(), name='login'),

    path('threshold', ThresholdCoefficientView.as_view(), name='threshold'),
    path('threshold/<int:pk>', ThresholdCoefficientView.as_view(), name='threshold-detail'),

    path('duration', SurgeDurationView.as_view(), name='duration'),

    path('surge', FactorView.as_view(), name='surge'),
]
