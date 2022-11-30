from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response

from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
# from .adapters import AppleOAuth2Adapter
from rest_auth.registration.views import (
    SocialLoginView,
    SocialConnectView
)

# from django.contrib.auth.models import Group

from accounts.models import User, UserProfile
from accounts.serializers import UserSerializer, UserProfileSerializer

# from accounts.permissions import IsLoggedInUserOrAdmin, IsAdminUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action == 'create':
    #         permission_classes = [IsAdminUser]
    #     elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
    #         permission_classes = [IsLoggedInUserOrAdmin]
    #     elif self.action == 'list' or self.action == 'destroy':
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action == 'create':
    #         permission_classes = [IsAdminUser]
    #     elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
    #         permission_classes = [IsLoggedInUserOrAdmin]
    #     elif self.action == 'list' or self.action == 'destroy':
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]


class AppleLogin(SocialLoginView):
    adapter_class = AppleOAuth2Adapter


class AppleConnect(SocialConnectView):
    adapter_class = AppleOAuth2Adapter