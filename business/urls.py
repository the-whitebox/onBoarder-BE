from django.urls import path, include

from rest_framework import routers
from business.views import (BusinessRegistrationViewSet,
                            BusinessLocation,
                            DuplicateSettings,
                            SearchMembers,ShowSchedules,
                            ShiftViewSet,ShowSchedulesByDate,
                            RemoveEmptyShifts,MarkEmptyShiftsAsOpen,
                            ShowStatsforShifts,PublishShift,
                            ShiftCopyView,ShiftImportView,DownloadWithCsv,
                            ShiftCloneView,SendOffers,ViewShiftHistory
                            ,SaveTemplate,LoadTemplate)

router = routers.DefaultRouter()
router.register(r'business', BusinessRegistrationViewSet, basename='business')
router.register(r'location', BusinessLocation, basename='location')
router.register(r'search_members', SearchMembers, basename='search_members')
router.register(r'shift', ShiftViewSet, basename='shift')
router.register(r'show_schedules', ShowSchedules, basename='show_schedules')
router.register(r'show_schedules_by_date', ShowSchedulesByDate, basename='show_schedules_by_date')
router.register(r'load_template', LoadTemplate, basename='load_template')

urlpatterns = [
    path('', include(router.urls)),
    path('duplicate_settings/', DuplicateSettings.as_view(), name='duplicate_settings'),
    path('remove_empty_shifts/', RemoveEmptyShifts.as_view(), name='remove_empty_shifts'),
    path('mark_empty_shifts_as_open/', MarkEmptyShiftsAsOpen.as_view(), name='mark_empty_shifts_as_open'),
    path('show_stats_for_shifts/', ShowStatsforShifts.as_view(), name='show_stats_for_shifts'),
    path('publish_shift/', PublishShift.as_view(), name='publish_shift'),
    path('copy_shifts/', ShiftCopyView.as_view(), name='copy_shifts'),
    path('import_shifts/', ShiftImportView.as_view(), name='import_shifts'),
    path('download_with_csv/', DownloadWithCsv.as_view(), name='download_with_csv'),
    path('clone_shift/', ShiftCloneView.as_view(), name='clone_shift'),
    path('send_offers/', SendOffers.as_view(), name='send_offers'),
    path('shift_history/', ViewShiftHistory.as_view(), name='shift_history'),
    path('save_template/', SaveTemplate.as_view(), name='save_template'),
]
