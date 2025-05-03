from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from common.throttling import PremiumUserRateThrottle
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_premium': user.profile.is_premium,
        }, status=status.HTTP_201_CREATED)


class CustomLogInView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [AnonRateThrottle]

class LogoutView(APIView):
    def get_throttles(self):
        if self.request.user.is_authenticated and self.request.user.profile.is_premium:
            throttle_classes = [PremiumUserRateThrottle]
        else:
            throttle_classes = [UserRateThrottle]
        return [throttle() for throttle in throttle_classes]

    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response({"message": "Successfully logged out!"})