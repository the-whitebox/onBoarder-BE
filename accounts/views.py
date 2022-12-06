from rest_framework import (
    viewsets, views,
    status, permissions
    )
from rest_framework.views import APIView
from rest_framework.response import Response

from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
# from .adapters import AppleOAuth2Adapter
from dj_rest_auth.registration.views import (
    SocialLoginView,
    SocialConnectView
)

# from django.contrib.auth.models import Group

from accounts.models import User, UserProfile
from accounts.serializers import UserSerializer, UserProfileSerializer

# from accounts.permissions import IsLoggedInUserOrAdmin, IsAdminUser
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction

import logging
LOG = logging.getLogger('accounts.views')

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

class UserRegistartionView(APIView):
    permission_classes = (permissions.AllowAny,)

    @transaction.atomic
    def post(self, *args, **kwargs):
        try:
            username = self.request.POST.get('username', None)
            email = self.request.POST.get('email', None)
            if User.objects.filter(email=email).exists() or email is None:
                return Response({'data': f"User with {email} already exist."}, status.HTTP_400_BAD_REQUEST)
            user_profile = UserProfile.objects.create()
            user = User.objects.create(email=email, username=username, is_admin=True, profile=user_profile)
            password = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
            user.set_password(password)
            user.save()

            email_sent = send_mail(
                'Your Deputy login details',
                f"Hi Muhammad Tahir,\n\nWelcome to your Deputy trial! We're excited to get you up and running.\nBelow you’ll find your account login information. You’ll need these details to log in on our Web or Mobile Apps.\nYour temporary password:\n\nEmail address: {email}\nPassword: {password}\n\nHappy scheduling!\nThe Deputy Team",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently = False,
            )

            return Response({'data': "User created successfully, please check you email for login credentials"}, status.HTTP_200_OK)
            
        except Exception as e:
            LOG.error('User %s: Profile is not created' % (username,))
            return Response({'error': e},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)