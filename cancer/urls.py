from django.urls import path
from . import views

urlpatterns = [
    path('BCindex/', views.BCindex, name='BCindex'),
    path('BCpre/', views.BCpre, name='BCpre'),
    path('HDindex/', views.HDindex, name='HDindex'),
    path('HDpre/', views.HDpre, name='HDpre'),
    path('HEindex/', views.HEindex, name='HEindex'),
    path('HEpre/', views.HEpre, name='HEpre'),
]
