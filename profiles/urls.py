from django.urls import path
from . import views


urlpatterns = [
    path('auth/register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('auth/login/', views.CustomLogInView.as_view(), name='user-login'),
    path('auth/logout/', views.LogoutView.as_view(), name='user-login'),
]
