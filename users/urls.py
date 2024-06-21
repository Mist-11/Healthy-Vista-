from django.urls import path
from . import views

urlpatterns = [
    path('login_page/', views.login_page, name='login'),
    path('login/', views.login),
    path('register/', views.register),
    path('register_page/', views.register_page, name='register'),
    path('logout/', views.logout, name='logout'),
    path('', views.index, name='index'),
    path('usercenter_page/', views.usercenter_page, name='usercenter'),
    path('find_detail_record/<str:username>/<str:timestamp>/', views.find_detail_record, name='find_detail_record'),
    path('help_page/', views.help_page, name='help_page'),
    path('singlecreate/', views.single_create, name='singlecreate'),
    path('batchcreate/', views.batch_create, name='batchcreate'),
    path('sendcode/', views.sendcode, name='sendcode'),
    path('receivecode/', views.receivecode, name='receivecode'),
    path('forget_page/', views.forget_page, name='forget')
]
