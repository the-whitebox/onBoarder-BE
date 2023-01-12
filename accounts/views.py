from rest_framework import (
    viewsets, views,
    status, permissions
    )
from rest_framework.views import APIView
from rest_framework.response import Response

from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from .adapters import AppleOAuth2Adapter
from dj_rest_auth.registration.views import (
    SocialLoginView,
    SocialConnectView
)

# from django.contrib.auth.models import Group

from accounts.models import (
    User, UserProfile, ENUMS, Role
    )
from accounts.serializers import (
    UserSerializer, UserProfileSerializer,
    ENUMSerializer
    )

# from accounts.permissions import IsLoggedInUserOrAdmin, IsAdminUser
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from rest_framework.decorators import action
from django.utils.crypto import get_random_string
from django.db.models import Q

import logging
LOG = logging.getLogger('accounts.views')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super(UserViewSet, self).get_queryset()
        if self.request.GET.get('business_id', None):
            return User.objects.filter(business__id=self.request.GET.get('business_id'))
        return queryset
    
    @action(methods=['patch'], detail=False)
    def bulk_update(self, request):

        data = {  # we need to separate out the id from the data
            i['id']: {k: v for k, v in i.items() if k != 'id'}
            for i in request.data
        }
        response = []
        for inst in self.get_queryset().filter(id__in=data.keys()):
            serializer = self.get_serializer(inst, data=data[inst.id], partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response.append(serializer.data)

        return Response(response, status=status.HTTP_200_OK)

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

class ENUMSViewSet(viewsets.ModelViewSet):
    queryset = ENUMS.objects.all()
    serializer_class = ENUMSerializer


class AppleLogin(SocialLoginView):
    adapter_class = AppleOAuth2Adapter


class AppleConnect(SocialConnectView):
    adapter_class = AppleOAuth2Adapter

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class GoogleConnect(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter

class UserRegistartionView(APIView):
    permission_classes = (permissions.AllowAny,)

    @transaction.atomic
    def post(self, *args, **kwargs):
        try:
            username = self.request.data.get('username')
            email = self.request.data.get('email')
            if User.objects.filter(Q(email=email) | Q(username=username)).exists():
                return Response({'data': f"User with {email} or {username} already exist."}, status.HTTP_400_BAD_REQUEST)
            user_profile = UserProfile.objects.create()
            try:
                role = Role.objects.get(role=Role.SYSTEM_ADMINISTRATOR)
            except Role.DoesNotExist:
                LOG.error('User Role Does not exist for: %s' % username)
                return Response({'error': 'profile_not_found'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            user = User.objects.create(email=email, role=role, username=username, profile=user_profile)
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
            print("message", e)
            LOG.error('User %s: Profile is not created' % (username,), e)
            return Response({'error': 'Profile is not created'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

class InvitationLinkView(APIView):
    def post(self, *args, **kwargs):
        try:
            try:
                user = User.objects.get(pk=self.request.user.id)
                unique_id = get_random_string(length=64)
                user.profile.invitation_key = unique_id
                user.profile.save()
            except User.DoesNotExist:
                LOG.error('User Does not exist')
                return Response({'error': 'user_not_found'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'invitation_link': f'http://127.0.0.1:8000/{unique_id}'}, status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': 'Link is not created'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, *args, **kwargs):
        try:
            try:
                user = User.objects.get(pk=self.request.user.id)
                user.profile.invitation_key = None
                user.profile.save()
            except User.DoesNotExist:
                LOG.error('User Does not exist')
                return Response({'error': 'user_not_found'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'invitation_link': user.profile.invitation_key}, status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': 'Link is not deleted'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        
import csv
import codecs
class CsvReader(APIView):

    def post(self,request):
        file_obj = request.FILES['csv']
        print(type(file_obj))
        return Response(status=204)

    def get(self,request,*args, **kwargs):
        file = request.FILES['csv']
        reader = csv.reader(codecs.iterdecode(file, 'utf-8'))
        data = []
        for row in reader:
            dict = {"name": row[0],
            "email": row[1],"phone_number": row[2],"role": row[3]}
            data.append(dict)
        return Response(data, status=status.HTTP_200_OK)

class CsvNewUsers(APIView):
    def post(self,request ,*args, **kwargs):
        data = self.request.data
        for row in data:
            username=row.get('username', None)
            email=row.get('email', None)
            phone_number=row.get('phone_number', None)
            role=row.get('role', None)
            if username is not None or email is not None or role is not None or phone_number is not None:
                try:
                    role = Role.objects.get(role=role)
                    user = User.objects.create(username=username,email=email,role=role)
                    user.profile.phone_number = phone_number
                    user.save()
                except Role.DoesNotExist:
                    LOG.error('Role Does not exist')
                    return Response({'error': f"{username} has no Valid Role, That's why Users not Created"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                email_sent = send_mail(
                    'Dupty',
                    f"welcome to deputy. You have been added as Team members with Email address: {email}",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently = False,
                )
            else:
                return Response({'Message': "Parameters missing"}, status.HTTP_400_BAD_REQUEST)

        return Response({'data': "User added successfully, please check your email",'email':email_sent}, status.HTTP_200_OK)
