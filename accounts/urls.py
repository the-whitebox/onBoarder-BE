from django.urls import path, include

from rest_framework import routers

from rest_auth.registration.views import (
    SocialAccountListView, SocialAccountDisconnectView
)
from accounts.views import (
    UserViewSet, UserProfileViewSet,
    AppleLogin, AppleConnect
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'user_profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/', include('rest_auth.urls')),
    path('accounts/', include('allauth.urls')),

    path('auth/apple/', AppleLogin.as_view(), name='apple_login'),
    path('auth/apple/connect/', AppleConnect.as_view(), name='apple_connect'),
    
    path('socialaccounts/', SocialAccountListView.as_view(), name='social_account_list'),
    path('socialaccounts/<int:pk>/disconnect/', SocialAccountDisconnectView.as_view(),
         name='social_account_disconnect')
]