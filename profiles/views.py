from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
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


# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         try:
#             token = request.auth
#
#             OutstandingToken.objects.filter(token=token).update(blacklisted=True)
#             return Response({"detail": "Successfully logged out."}, status=200)
#         except Exception as e:
#             return Response({"detail": "Failed to log out."}, status=400)


class LogoutView(APIView):
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response({"message": "tizimdan chiqdiz"})