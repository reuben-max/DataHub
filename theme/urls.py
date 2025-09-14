from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('browse/', views.browse_view, name='browse'),
    path('upload/', views.upload_view, name='upload'),
    path('logout/', views.logout_view, name='logout'),
]
