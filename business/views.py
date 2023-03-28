from django.shortcuts import render
from business.models import Business,Location
from business.serializers import BusinessSerializer,LocationSerializer
from rest_framework import (
    viewsets, views,
    status, permissions
    )

# Create your views here.
class BusinessRegistrationViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

    # def perform_create(self, serializer):
    #     return serializer.save(user = self.request.user)


class BusinessLocation(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
