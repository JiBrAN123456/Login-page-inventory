# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterAPIView, LoginAPIView, ProfileAPIView


urlpatterns = [
    # Register endpoint
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    
    # Login endpoint (JWT)
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    
    # Profile endpoint
    path('auth/profile/', ProfileAPIView.as_view(), name='profile'),

      path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
