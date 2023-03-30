from django.urls import path, include

from rest_framework import routers
from business.views import BusinessRegistrationViewSet,BusinessLocation,CopySettings

router = routers.DefaultRouter()
router.register(r'business', BusinessRegistrationViewSet, basename='business')
router.register(r'location', BusinessLocation, basename='location')


urlpatterns = [
    path('', include(router.urls)),
    path('copy_settings/', CopySettings.as_view(), name='copy_settings')
]