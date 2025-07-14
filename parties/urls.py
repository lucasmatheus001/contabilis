"""
URL configuration for parties app.
"""

from django.urls import path
from . import views

app_name = 'parties'

urlpatterns = [
    path('', views.party_list, name='party_list'),
    path('create/', views.party_create, name='party_create'),
    path('<int:pk>/', views.party_detail, name='party_detail'),
    path('<int:pk>/update/', views.party_update, name='party_update'),
    path('<int:pk>/delete/', views.party_delete, name='party_delete'),
] 