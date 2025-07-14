"""
URL configuration for processes app.
"""

from django.urls import path
from . import views

app_name = 'processes'

urlpatterns = [
    path('', views.process_list, name='process_list'),
    path('create/', views.process_create, name='process_create'),
    path('<int:pk>/', views.process_detail, name='process_detail'),
    path('<int:pk>/update/', views.process_update, name='process_update'),
    path('<int:pk>/delete/', views.process_delete, name='process_delete'),
    path('export/', views.export_processes, name='export_processes'),
] 