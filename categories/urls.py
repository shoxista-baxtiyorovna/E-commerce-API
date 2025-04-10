from django.urls import path
from . import views


urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='list'),
    path('categories/<int:pk>/', views.CategoryRetrieveView.as_view(), name='retrieve')
]