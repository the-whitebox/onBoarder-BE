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
    User, UserProfile, ENUMS, Role, Document
    )

from employment.models import (
    UserWorkDetail, UserPayDetail,
    UserWorkingHours, UserLeaveEntitlements,
    HourlyPayRate, HourlyOneAndHalfOvertimePayRate,
    SalaryPayRate, FixedPayRate, 
    HourlyFortyFourHourOvertimePayRate, PerDayPayRate,
    WorkPeriod
)

from accounts.serializers import (
    UserSerializer, UserProfileSerializer,
    ENUMSerializer,RoleSerializer
    )

# from accounts.permissions import IsLoggedInUserOrAdmin, IsAdminUser
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from rest_framework.decorators import action
from django.utils.crypto import get_random_string
from django.db.models import Q
from rest_framework.decorators import authentication_classes, permission_classes
from datetime import datetime, timedelta

import logging
LOG = logging.getLogger('accounts.views')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        business_id = self.request.GET.get('business_id',None)
        if business_id:
            queryset =  User.objects.filter(business=business_id)
            return queryset
        else:
            queryset = User.objects.all()
            return queryset

    @action(methods=['patch'], detail=False)
    def bulk_update(self, request):
        print("this is bulk update")
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
@authentication_classes([])
@permission_classes([])
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
import os
from rest_framework_simplejwt.tokens import RefreshToken
from dotenv import load_dotenv

load_dotenv()
Host = os.getenv('Host')

class UserRegistartionView(APIView):
    permission_classes = (permissions.AllowAny,)

    @transaction.atomic
    def post(self,request, *args, **kwargs):
        try:
            username = self.request.data.get('username')
            email = self.request.data.get('email')
            password = self.request.data.get('password')

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

            work_detail = UserWorkDetail.objects.create(user=user)
            hourly_pay_rate = HourlyPayRate.objects.create()
            hourly_one_and_half_overtime_pay_rate = HourlyOneAndHalfOvertimePayRate.objects.create()
            salary_pay_rate = SalaryPayRate.objects.create()
            fixed_pay_rate = FixedPayRate.objects.create()
            hourly_forty_four_hour_overtime_rate = HourlyFortyFourHourOvertimePayRate.objects.create()
            per_day_pay_rate = PerDayPayRate.objects.create()
            pay_detail = UserPayDetail.objects.create(user=user, hourly_pay_rate=hourly_pay_rate, hourly_one_and_half_overtime_pay_rate=hourly_one_and_half_overtime_pay_rate,
            salary_pay_rate=salary_pay_rate, fixed_pay_rate=fixed_pay_rate, hourly_forty_four_hour_overtime_rate=hourly_forty_four_hour_overtime_rate,
            per_day_pay_rate=per_day_pay_rate)
            work_period = WorkPeriod.objects.create(user=user)
            working_hours = UserWorkingHours.objects.create(work_period=work_period, user=user)
            leave_entitlements = UserLeaveEntitlements.objects.create(user=user)

            if password:
                user.set_password(password)
                user.save()
            else:
                password = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                user.set_password(password)
                user.save()
            try:
                if request.FILES['image'] is not None:
                    print(request.FILES['image'])
                    myuser = UserProfile.objects.get(user=user)
                    Document.objects.create(content_object=myuser, image=request.FILES['image'])
                        # return Response("image saved")
            except:
                pass
            token = get_random_string(length=32)
            verify_link = Host + "verify_email/"+ token
            print(verify_link)
            user.email_verified_hash = token
            user.save()
            email_sent = send_mail(
                'Your MaxPilot login details',
                f"Hi Muhammad Tahir,\n\nWelcome to your MaxPilot trial! We're excited to get you up and running.\nBelow you’ll find your account login information. You’ll need these details to log in on our Web or Mobile Apps.\nConfrm you email by clicking this link \n {verify_link}\nYour temporary password:\n\nEmail address: {email}\nPassword: {password}\n\nHappy scheduling!\nThe MaxPilot Team",
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
# Verification of E-mail
import json
from django.http import JsonResponse
class VerificationEmail(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self,request):
            data = json.loads(request.body.decode('utf-8'))
            if data:
                token = data['token']
            else:
                return Response("Please provide token")
            time_threshold = datetime.now() - timedelta(hours=12)
            if User.objects.filter(email_verified_hash=token, email_verified=0, created_on__gte=time_threshold).exists():
                tokenExists = User.objects.get(email_verified_hash=token, email_verified=0)
                refresh = RefreshToken.for_user(tokenExists)
                access = str(refresh.access_token)
                tokenExists.email_verified = 1
                tokenExists.save()                
                res = {
                'status': 'success',
                'message': 'Valid',
                'user_id':tokenExists.id,
                "refresh": str(refresh),
                "access": str(access)
            }
            else:
                res = {
                    'status': 'failed',
                    'message': 'Invalid',
                }
            return JsonResponse(res) 

class VerificationLinkEmail(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self,request):
            email = self.request.GET.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                if user.email_verified == True:
                    return Response({'data': "User is already verified"}, status.HTTP_200_OK)
                else:
                    token = get_random_string(length=32)
                    verify_link = Host + "verify_email/"+ token
                    user.email_verified_hash = token
                    user.save()
                    email_sent = send_mail(
                        'Your MaxPilot login details',
                        f"Hi Muhammad Tahir,\n\nWelcome to your MaxPilot trial! We're excited to get you up and running.\nBelow you’ll find your account login information. You’ll need these details to log in on our Web or Mobile Apps.\nConfrm you email by clicking this link \n {verify_link}\n\nEmail address: {user.email}\n\nHappy scheduling!\nThe MaxPilot Team",
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently = False,
                    )
                    return Response({'data': "please check you email for login credentials"}, status.HTTP_200_OK)
            else:
                return Response({'data': "user does not exists,please signup for user creation"}, status.HTTP_200_OK)
                
# Custom login
from dj_rest_auth.views import LoginView
from rest_framework.authtoken.models import Token

class CustomLoginView(LoginView):
    def get_response(self):
        self.serializer.is_valid(raise_exception=True)
        user = self.serializer.validated_data['user']
        orginal_response = super().get_response()
        print(user.email_verified)
        if user.email_verified == False:
            return Response({'detail': 'User not verified.'},status=status.HTTP_401_UNAUTHORIZED)
        mydata = {"message": "Login Successful", "status": "success"}
        orginal_response.data.update(mydata)
        return orginal_response

    # def login(self):
    #     print("this")
    #     self.serializer.is_valid(raise_exception=True)
    #     user = self.serializer.validated_data['user']
    #     token, created = Token.objects.get_or_create(user=user)
    #     if user.email_verified == True:
            
    #         return Response({'detail': 'User account is Login.'}, status=status.HTTP_401_UNAUTHORIZED)

    #     return Response({'key': token.key})

class InvitationLinkView(APIView):
    def get(self, *args, **kwargs):
        try:
            try:
                user = User.objects.get(pk=self.request.user.id)
            except User.DoesNotExist:
                LOG.error('User Does not exist')
                return Response({'error': 'user_not_found'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            unique_id = user.profile.invitation_key
            return Response({'invitation_link': f'http://127.0.0.1:8000/{unique_id}'}, status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Link is not created'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        return Response(status=status.HTTP_204_NO_CONTENT)

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
                    f"welcome to MaxPilot. You have been added as Team members with Email address: {email}",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently = False,
                )
            else:
                return Response({'Message': "Parameters missing"}, status.HTTP_400_BAD_REQUEST)

        return Response({'data': "User added successfully, please check your email",'email':email_sent}, status.HTTP_200_OK)

class EnumsReturn(APIView):
    def get(self,request ,*args, **kwargs):
        group = self.request.GET.get('group',None)
        all_data=[]
        if group:
            data = ENUMS.objects.filter(group=group)
            for d in data:
                response = {"name":d.name, "reference_id":d.reference_id, "group":d.group}
                all_data.append(response)
            return Response(all_data, status.HTTP_200_OK)
        else:
            return Response({'Message': "Parameters missing"}, status.HTTP_400_BAD_REQUEST)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
