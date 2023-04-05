from django.shortcuts import render
from accounts.models import User
from business.models import Business,Location,Area,OperatingHours
from business.serializers import BusinessSerializer,LocationSerializer
from accounts.serializers import UserSerializer
from rest_framework import (
    viewsets, views,
    status, permissions
    )
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from employment.models import UserWorkingHours,UserPayDetail
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
            operating_hour = location.operating_hours
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

    def post(self, request):
        # Get the ID of the instance to duplicate
        id = request.data.get('id', None)
        # Get the instance to duplicate
        try:
            location = Location.objects.get(id=id)
            print(location)
            areas = location.areas.all()
            print(areas)
            users = location.people.all()
            operating_hours = location.operating_hours.all()
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
        return Response({"Object dublicated successfully"})
    

# Schedule Apis
class SearchMembers(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self,):
        location_id = self.request.GET.get('location_id', None)
        area = self.request.GET.get('area', None)
        if location_id:
            if area:
                queryset = User.objects.filter(user_location=location_id)
            # else:
            #     queryset = User.objects.filter(user_location=location_id)
            return queryset
        
        else:
            location = Location.objects.all()
            for data in location:
                users = User.objects.filter(user_location=data)
                
            return users


class ShowSchedules(APIView):
    def get(self,request ,*args, **kwargs):
        location_id = self.request.data.get('location_id',None)
        all_members=[]
        location = Location.objects.get(id=location_id)

        try:
            if location:
                users = User.objects.filter(user_location=location)
            else:
                users = User.objects.all()
            for user in users:
                userworkinghours = UserWorkingHours.objects.get(user=user)
                stress = userworkinghours.stress_level
                total_hours = userworkinghours.total_hours_for_work_period
                base_pay = UserPayDetail.objects.get(user=user).hourly_pay_rate.weekday_rate
                response = {"username":user.username,"Total hours": total_hours,"Base Pay": base_pay,"Stress":stress}
                all_members.append(response)
            return Response(all_members, status.HTTP_200_OK)
        except:
            return Response({'Message': "Bad Request"}, status.HTTP_400_BAD_REQUEST)


