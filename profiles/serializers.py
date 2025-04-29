from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_premium = serializers.BooleanField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_premium']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.profile.is_premium = validated_data.get('is_premium', False)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        refresh = self.get_token(user)
        return {
        "token": str(refresh.access_token),
        "user_id": user.id,
        "username": user.username,
        "is_premium": user.profile.is_premium,
        }


