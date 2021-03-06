from loguru import logger
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from main.models import Threshold
from main.serializers import (
    FactorSerializer,
    RegisterSerializer,
    SurgeDurationSerializer,
    ThresholdCoefficientSerializer,
)
from utils.functions import (
    find_coefficient,
    district_requests,
    find_district_by_database,
    set_redis_surge_duration,
    get_redis_surge_duration,
)


class FactorView(APIView):
    def get(self, request):
        logger.info(f'Request query_params:{request.query_params}')

        serializer = FactorSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        lat, lon = serializer.validated_data['lat'], serializer.validated_data['lon']

        district = find_district_by_database(lat, lon)
        logger.info(f'District is {district}')

        request_count = district_requests(district)
        logger.info(f'Request count in District {district} is {request_count}')

        coefficient = find_coefficient(request_count)
        logger.info(f'Coefficient for District {district} is {coefficient}')

        return Response({'coefficient': coefficient})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class SurgeDurationView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = SurgeDurationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        duration = serializer.validated_data['duration']
        set_redis_surge_duration(duration)
        logger.info(f'User {request.user.username} set duration to {duration}')

        return Response({'message': f'surge time set for last {duration} minutes'}, status=HTTP_201_CREATED)

    @staticmethod
    def get(request):
        duration = get_redis_surge_duration()
        return Response({'message': f'surge time set for last {duration} minutes'})


class ThresholdCoefficientView(APIView):
    serializer = ThresholdCoefficientSerializer
    query = Threshold.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f'User {request.user.username} set a new threshold: {serializer.data}')

        return Response(serializer.validated_data, status=HTTP_201_CREATED)

    def get(self, request):
        serializer = self.serializer(self.query, many=True)
        return Response(serializer.data)

    @staticmethod
    def delete(request, pk):
        threshold = get_object_or_404(Threshold, id=pk)
        threshold.delete()
        logger.info(f'User {request.user.username} delete a threshold with ID {pk}')

        return Response({'message': 'deleted'}, status=HTTP_204_NO_CONTENT)
