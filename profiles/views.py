from django.contrib.auth.models import User
from django.contrib.auth import logout
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

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


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)  # This will end the session and clear the session cookie
        return Response({"detail": "Successfully logged out."})