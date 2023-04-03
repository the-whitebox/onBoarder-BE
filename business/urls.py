from django.urls import path, include

from rest_framework import routers
from business.views import BusinessRegistrationViewSet,BusinessLocation,DuplicateSettings

router = routers.DefaultRouter()
router.register(r'business', BusinessRegistrationViewSet, basename='business')
router.register(r'location', BusinessLocation, basename='location')


urlpatterns = [
    path('', include(router.urls)),
    path('duplicate_settings/', DuplicateSettings.as_view(), name='duplicate_settings')

]