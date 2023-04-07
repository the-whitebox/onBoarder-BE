from django.urls import path, include

from rest_framework import routers
from business.views import BusinessRegistrationViewSet,BusinessLocation,DuplicateSettings,SearchMembers,ShowSchedules,ShiftViewSet,ShowSchedulesByDate,RemoveEmptyShifts,MarkEmptyShiftsAsOpen,ShowStatsforShifts

router = routers.DefaultRouter()
router.register(r'business', BusinessRegistrationViewSet, basename='business')
router.register(r'location', BusinessLocation, basename='location')
router.register(r'search_members', SearchMembers, basename='search_members')
router.register(r'shift', ShiftViewSet, basename='shift')
router.register(r'show_schedules', ShowSchedules, basename='show_schedules')
# router.register(r'view_by_area_team_members', ViewByAreaTeamMembers, basename='view_by_area_team_members')
router.register(r'show_schedules_by_date', ShowSchedulesByDate, basename='show_schedules_by_date')

urlpatterns = [
    path('', include(router.urls)),
    path('duplicate_settings/', DuplicateSettings.as_view(), name='duplicate_settings'),
    path('remove_empty_shifts/', RemoveEmptyShifts.as_view(), name='remove_empty_shifts'),
    path('mark_empty_shifts_as_open/', MarkEmptyShiftsAsOpen.as_view(), name='mark_empty_shifts_as_open'),
    path('show_stats_for_shifts/', ShowStatsforShifts.as_view(), name='show_stats_for_shifts')
]
