from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='list'),
    path('products/<int:pk>/', views.ProductRetrieveView.as_view(), name='retrieve'),
    path('products/search/', views.ProductSearchView.as_view(), name='search'),
]