from django.urls import path
from . import views


urlpatterns = [
    path('cart/', views.ListView.as_view(), name='list'),
    path('cart/add/', views.CreateView.as_view(), name='add')
]