from django.urls import path, include,re_path
from rest_framework import routers

from dj_rest_auth.registration.views import (
    SocialAccountListView, SocialAccountDisconnectView,VerifyEmailView
)

from dj_rest_auth.views import PasswordResetConfirmView

from accounts.views import (
    UserViewSet, UserProfileViewSet,
    AppleLogin, AppleConnect,
    GoogleLogin, GoogleConnect,
    UserRegistartionView, ENUMSViewSet,
    InvitationLinkView,CsvReader,
    CsvNewUsers,EnumsReturn,RoleViewSet
)

router = routers.DefaultRouter()
router.register(r'people', UserViewSet, basename='user')
router.register(r'user_profiles', UserProfileViewSet)
router.register(r'enums', ENUMSViewSet, basename='enums')
router.register(r'role', RoleViewSet, basename='role')

# router.register(r'EnumsReturn', EnumsReturn)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/user/registration/', UserRegistartionView.as_view()),
    path('auth/verify_email/', VerifyEmailView.as_view(),name='rest_verify_email'),
    path('auth/account_confirm_email/', VerifyEmailView.as_view(),name='account_email_verification_sent'),
    re_path(r'^auth/user/registration/account-confirm-email/(?P<key>[-:\w]+)/$',
         VerifyEmailView.as_view(), name='account_confirm_email'),

    path('invitation_link/', InvitationLinkView.as_view()),
    # path('auth/business/registration/', ),
    path('accounts/', include('allauth.urls')),
    path("invitations/", include('invitations.urls', namespace='invitations')),

    path('auth/apple/', AppleLogin.as_view(), name='apple_login'),
    path('auth/apple/connect/', AppleConnect.as_view(), name='apple_connect'),

    path('auth/google/', GoogleLogin.as_view(), name='google_login',),
    path('auth/google/connect/', GoogleConnect.as_view(), name='google_connect'),
    
    path('socialaccounts/', SocialAccountListView.as_view(), name='social_account_list'),
    path('socialaccounts/<int:pk>/disconnect/', SocialAccountDisconnectView.as_view(),
         name='social_account_disconnect'),

    # path('upload/', UploadFileView.as_view(), name='upload-file'),
    path('csvreader/', CsvReader.as_view(), name='CsvReader'),
    path('csvnewusers/', CsvNewUsers.as_view(), name='csvnewusers'),
    path('EnumsReturn/', EnumsReturn.as_view(), name='EnumsReturn')

]