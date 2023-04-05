from django.urls import path, include

from rest_framework import routers
from business.views import BusinessRegistrationViewSet,BusinessLocation,DuplicateSettings,SearchMembers,ShowSchedules

router = routers.DefaultRouter()
router.register(r'business', BusinessRegistrationViewSet, basename='business')
router.register(r'location', BusinessLocation, basename='location')
router.register(r'search_members', SearchMembers, basename='search_members')


urlpatterns = [
    path('', include(router.urls)),
    path('duplicate_settings/', DuplicateSettings.as_view(), name='duplicate_settings'),
    # path('search_members/', SearchMembers.as_view(), name='search_members'),
    path('show_schedules/', ShowSchedules.as_view(), name='show_schedules')

]
