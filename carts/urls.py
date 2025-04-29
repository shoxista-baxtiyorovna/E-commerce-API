from django.urls import path
from . import views


urlpatterns = [
    path('cart/', views.CartListView.as_view(), name='list'),
    path('cart/add/', views.AddToCartView.as_view(), name='add')
]