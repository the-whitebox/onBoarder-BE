from django.shortcuts import render
from accounts.models import User
from business.models import Business,Location,Area,OperatingHours
from business.serializers import BusinessSerializer,LocationSerializer,OperatingHourSerializer
from rest_framework import (
    viewsets, views,
    status, permissions
    )
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes

# Create your views here.
@authentication_classes([])
@permission_classes([])
class BusinessRegistrationViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

    # def perform_create(self, serializer):
    #     return serializer.save(user = self.request.user)


class BusinessLocation(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def patch(self, request, *args, **kwargs):
        source_id = request.data.get('source_id')
        destination_ids = request.data.get('destination_ids')
        location = Location.objects.get(id=source_id)
        operating_hours = OperatingHours.objects.filter(location=location)
        for id in destination_ids:
            location = Location.objects.get(id=id)
            operating_hour = location.operating_hours_location
            related_objects = operating_hour.all()

            for hours in operating_hours:
                for related_obj in related_objects:
                    related_obj.days = hours.days
                    related_obj.start_time = hours.start_time
                    related_obj.end_time = hours.end_time
                    related_obj.is_closed = hours.is_closed
                    related_obj.save()

        return Response({'Message': "Operating hours copied sucessfully"}, status.HTTP_200_OK)



class DuplicateSettings(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def create(self, request, *args, **kwargs):
        # Get the ID of the instance to duplicate
        id = request.data.get('id', None)
        print(id)

        # Get the instance to duplicate
        location = Location.objects.get(id=id)
        area = location.area_location
        people = location.user_location
        operating_hours = location.operating_hours_location
        
        print(area)
        # Create a new instance as a duplicate of the existing instance
        new_instance = Location.objects.create(
            location_name=request.data.get('name', None),
            location_code=location.location_code,
            location_address=location.location_address,
            timezone=location.timezone,
            location_week_starts_on=location.location_week_starts_on,
            business_location=location.business_location,


            physical_address=area.physical_address,
            area_of_work=area.area_of_work,
            address=area.address,
            people=people.people,
            is_closed=operating_hours.is_closed,
            days=operating_hours.days,
            start_time=operating_hours.start_time,
            end_time=operating_hours.end_time,
            location=operating_hours.location,
        )
        new_instance.save()
        # Return the response with the serialized data of the new instance
        serializer = self.get_serializer(new_instance)
        return Response(serializer.data)