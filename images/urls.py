from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', views.login_view, name='api-login'),
    path('auth/logout/', views.logout_view, name='api-logout'),
    path('auth/register/', views.register_view, name='api-register'),
    path('auth/profile/', views.user_profile_view, name='user-profile'),
    
    # ImageSet endpoints
    path('imagesets/', views.ImageSetListCreateView.as_view(), name='imageset-list-create'),
    path('imagesets/<int:pk>/', views.ImageSetDetailView.as_view(), name='imageset-detail'),
    
    # Image upload endpoints
    path('imagesets/<int:image_set_id>/images/', views.ImageUploadView.as_view(), name='image-upload'),
    path('images/<int:pk>/', views.ImageDeleteView.as_view(), name='image-delete'),
]
