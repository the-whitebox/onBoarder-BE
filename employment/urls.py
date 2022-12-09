from django.urls import path, include

from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'business', BusinessRegistrationViewSet, basename='business')

urlpatterns = [
    path('', include(router.urls)),
]