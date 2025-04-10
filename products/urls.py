from django.urls import path
from . import views


urlpatters = [
    path('products/', views.ProductListView.as_view(), name='list'),
    path('products/<int:pk>/', views.ProductRetrieveView.as_view(), name='retrieve'),
]