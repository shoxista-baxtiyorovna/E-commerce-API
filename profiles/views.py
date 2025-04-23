from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from .permissions import IsPremiumUser


class PremiumContentView(APIView):
    permission_classes = [IsAuthenticated, IsPremiumUser, AllowAny]

    def get(self, request):
        return Response({"message": "You have access to premium content!"})



class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_premium': user.is_premium,
            'access': access_token,
            'refresh': refresh_token
        }, status=status.HTTP_201_CREATED)
