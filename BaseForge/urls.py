# project/urls.py (main URL configuration)
from django.contrib import admin
from django.urls import path, include

# Define the API-related URL patterns
api_urlpatterns = [
    path('auth/', include('authcore.urls')),  # Including authcore app URLs under 'api/auth/'
    path('fintrack/', include('fintrack.urls')),  # Including fintrack app URLs under 'api/fintrack/'
]

from django.urls import path
from authcore.google_service import GoogleLoginAPIView, OAuthCallbackAPIView

# Main URL configuration
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),  # Include the API patterns under 'api/'
    path('api/google-login/', GoogleLoginAPIView.as_view(), name='google_login'),
    path('api/oauth/callback/', OAuthCallbackAPIView.as_view(), name='oauth_callback'),
]
