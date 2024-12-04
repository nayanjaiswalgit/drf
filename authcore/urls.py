from django.urls import path
from . import views



from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    #Authentication
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('logout/', views.LogoutView.as_view(), name='auth_logout'),
    path('profile/', views.getProfile, name='profile'),
    path('profile/update/', views.updateProfile, name='update-profile'),
   
]