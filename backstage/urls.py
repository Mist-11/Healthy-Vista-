from django.urls import path
from . import views

urlpatterns = [
    path('', views.backstageindex, name='backstageindex'),
    path('recentrecord/', views.recent_record),
    path('count/', views.count),
    path('searchuser/', views.searchuser),
    path('detailuser/', views.detailuser),
]