from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from main.models import Threshold


class FactorSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
        )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class SurgeDurationSerializer(serializers.Serializer):
    duration = serializers.IntegerField()

    @staticmethod
    def validate_duration(duration):
        if 1440 < duration or duration < 1:
            raise ValidationError('Enter a valid duration between 1 to 1440')
        return duration

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ThresholdCoefficientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threshold
        fields = (
            'request_count',
            'coefficient',
        )
