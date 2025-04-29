from django.urls import path
from . import views


urlpatterns = [
    path('orders/', views.OrderView.as_view(), name='order-list'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order-create'),
]