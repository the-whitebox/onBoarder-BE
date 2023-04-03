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

class DuplicateSettings(APIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer(Location, many=True)
    # def post(self, request):
    #     """
    #     Create a student record
    #     :param format: Format of the student records to return to
    #     :param request: Request object for creating student
    #     :return: Returns a student record
    #     """
    #     serializer = LocationSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save() 
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request):
        # Get the ID of the instance to duplicate
        id = request.data.get('id', None)
        # Get the instance to duplicate
        try:
            location = Location.objects.get(id=id)
            areas = location.area_location.all()
            users = location.user_location.all()
            operating_hours = location.operating_hours_location.all()
            # Create a new instance as a duplicate of the existing instance
            new_instance = Location.objects.create(
                location_name=request.data.get('location_name', None),
                location_code=location.location_code,
                location_address=location.location_address,
                timezone=location.timezone,
                location_week_starts_on=location.location_week_starts_on,
                business_location=location.business_location,
            )
            if new_instance:
                for area in areas:
                    myarea =  Area.objects.create(
                        physical_address=area.physical_address,
                        area_of_work=area.area_of_work,
                        address=area.address,  
                        location=location
                    )
                for people in users:
                    User.objects.filter(
                        user_location=people.user_location
                    )
                for operating_hour in operating_hours:
                    hours = OperatingHours.objects.create(
                        is_closed=operating_hour.is_closed,
                        days=operating_hour.days,
                        start_time=operating_hour.start_time,
                        end_time=operating_hour.end_time,
                        location=location,
                    )

        except: 
            return Response({"Object dublication failed"})

        new_instance.save()
        # Return the response with the serialized data of the new instance
        # serializer = self.get_serializer(new_instance)
        # print(serializer)
        return Response({"Object dublicated successfully"})