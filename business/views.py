from django.shortcuts import render
from accounts.models import User
from business.models import Business,Location,Area,OperatingHours,Shift
from business.serializers import BusinessSerializer,LocationSerializer,ShiftSerializer
from accounts.serializers import UserSerializer
from rest_framework import (
    viewsets, views,
    status, permissions
    )
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import filters
from datetime import timedelta
from django.utils import timezone
from dateutil.relativedelta import *
from rest_framework.decorators import action
from django.db import transaction
# Create your views here.
@authentication_classes([])
@permission_classes([])
class BusinessRegistrationViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

from rest_framework.generics import UpdateAPIView

class BusinessLocation(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def patch(self, request, *args, **kwargs):
        source_id = request.data.get('source_id')
        destination_ids = request.data.get('destination_ids')
        location = Location.objects.filter(id=source_id).first()
        operating_hours = location.operating_hours.all()
        try:
            for id in destination_ids:
                dest_location = Location.objects.filter(id=id).first()
                operating_hour = dest_location.operating_hours
                operating_hour.all().delete()
                operating_hour.set(operating_hours)
                dest_location.save()
                # serializer = self.get_serializer(dest_location)
                # return Response(serializer.data)
                return Response({'Message': "Operating hours copied sucessfully"}, status.HTTP_200_OK)
        except:
            return Response({'Message': "Operating hours did not copy"}, status.HTTP_400_BAD_REQUEST)

class DuplicateSettings(APIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer(Location, many=True)

    def post(self, request):
        id = request.data.get('id', None)
        try:
            location = Location.objects.get(id=id)
            areas = location.areas.all()
            users = location.people.all()
            print(users)
            operating_hours = location.operating_hours.all()
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
                        location=new_instance
                    )
                # for people in users:
                #     print(people)
                #     myusers = User.objects.filter(
                #             user_location=people
                #         ).first()
                # print(myusers)
                for operating_hour in operating_hours:
                    hours = OperatingHours.objects.create(
                        is_closed=operating_hour.is_closed,
                        days=operating_hour.days,
                        start_time=operating_hour.start_time,
                        end_time=operating_hour.end_time,
                        location=new_instance,
                    )
            new_instance.save()
            return Response("Object Duplicated") 
        except: 
            return Response({"Object dublication failed"},status=status.HTTP_400_BAD_REQUEST)

# Schedule Apis
class SearchMembers(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self,):
        location_id = self.request.GET.get('location_id', None)
        if location_id:
            queryset = User.objects.filter(user_location=location_id)
            return queryset
        else:
            all_location = Location.objects.all()
            all_users = []
            for location in all_location:
                people = User.objects.filter(user_location=location)
                for user in people:
                    all_users.append(user)
            return all_users

class ShowSchedules(viewsets.ModelViewSet):

    queryset = Shift.objects.all()
    filter_backends = [filters.SearchFilter]
    serializer_class = ShiftSerializer
    def get_queryset(self):
        area_id = self.request.GET.get('area_id', None)
        string = self.request.GET.get('string', None)
        location_id = self.request.GET.get('location_id', None)
        user = User.objects.filter(user_location=location_id).first()
        if location_id:
            if area_id:
                if string == "day_by_area":
                    today = timezone.now().date()      
                    shifts = Shift.objects.filter(start_date=today,location=location_id,area=area_id)
                    return shifts
                if string == "week_by_area":
                    today = timezone.now().date()
                    start_of_week = today - timezone.timedelta(days=today.weekday())
                    end_of_week = start_of_week + timezone.timedelta(days=6)
                    return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_week,location=location_id,area=area_id)
                if string == "two_weeks_by_area":
                    today = timezone.now().date()
                    start_of_week = today - timezone.timedelta(days=today.weekday())
                    end_of_2_week = start_of_week + timezone.timedelta(days=13)
                    return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_2_week,location=location_id,area=area_id)
                if string == "month_by_area":
                    current_date = timezone.now().date()
                    first_day_of_month = current_date.replace(day=1)
                    last_day_of_month = first_day_of_month + timedelta(days=32 - first_day_of_month.day)
                    last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
                    return Shift.objects.filter(start_date__gte=first_day_of_month,end_date__lte=last_day_of_month,location=location_id,area=area_id)
                
                if string == "day_by_team_member":
                    today = timezone.now().date()      
                    shifts = Shift.objects.filter(start_date__gte=today,location=location_id,area=area_id,user=user)
                    return shifts
                if string == "week_by_team_member":
                    today = timezone.now().date()
                    start_of_week = today - timezone.timedelta(days=today.weekday())
                    end_of_week = start_of_week + timezone.timedelta(days=6)
                    return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_week,location=location_id,area=area_id,user=user)
                if string == "two_weeks_by_team_member":
                    today = timezone.now().date()
                    start_of_week = today - timezone.timedelta(days=today.weekday())
                    end_of_2_week = start_of_week + timezone.timedelta(days=13)
                    return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_2_week,location=location_id,area=area_id,user=user)
                if string == "four_weeks_by_team_member":
                    today = timezone.now().date()
                    start_of_week = today - timezone.timedelta(days=today.weekday())
                    end_of_2_week = start_of_week + timezone.timedelta(days=27)
                    return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_2_week,location=location_id,area=area_id,user=user)
                if string == "month_by_team_member":
                    current_date = timezone.now().date()
                    first_day_of_month = current_date.replace(day=1)
                    last_day_of_month = first_day_of_month + timedelta(days=32 - first_day_of_month.day)
                    last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
                    return Shift.objects.filter(start_date__gte=first_day_of_month,end_date__lte=last_day_of_month,location=location_id,area=area_id,user=user)
            else:
                if string == "day_by_area":
                    today = timezone.now().date()      
                    shifts = Shift.objects.filter(start_date=today,location=location_id)
                    return shifts
                if string == "week_by_area":
                    today = timezone.now().date()
                    start_of_week = today - timezone.timedelta(days=today.weekday())
                    end_of_week = start_of_week + timezone.timedelta(days=6)
                    return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_week,location=location_id)
                if string == "two_weeks_by_area":
                    today = timezone.now().date()
                    start_of_week = today - timezone.timedelta(days=today.weekday())
                    end_of_2_week = start_of_week + timezone.timedelta(days=13)
                    return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_2_week,location=location_id)
                if string == "month_by_area":
                    current_date = timezone.now().date()
                    first_day_of_month = current_date.replace(day=1)
                    last_day_of_month = first_day_of_month + timedelta(days=32 - first_day_of_month.day)
                    last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
                    return Shift.objects.filter(start_date__gte=first_day_of_month,end_date__lte=last_day_of_month,location=location_id)
                
                if string == "day_by_team_member":
                    today = timezone.now().date()      
                    shifts = Shift.objects.filter(start_date=today,location=location_id,user=user)
                    return shifts
                if string == "week_by_team_member":
                    today = timezone.now().date()
                    start_of_week = today - timezone.timedelta(days=today.weekday())
                    end_of_week = start_of_week + timezone.timedelta(days=6)
                    return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_week,location=location_id,user=user)
                if string == "two_weeks_by_team_member":
                    today = timezone.now().date()
                    start_of_week = today - timezone.timedelta(days=today.weekday())
                    end_of_2_week = start_of_week + timezone.timedelta(days=13)
                    return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_2_week,location=location_id,user=user)
                if string == "four_weeks_by_team_member":
                    today = timezone.now().date()
                    start_of_week = today - timezone.timedelta(days=today.weekday())
                    end_of_2_week = start_of_week + timezone.timedelta(days=27)
                    return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_2_week,location=location_id,user=user)
                if string == "month_by_team_member":
                    current_date = timezone.now().date()
                    first_day_of_month = current_date.replace(day=1)
                    last_day_of_month = first_day_of_month + timedelta(days=32 - first_day_of_month.day)
                    last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
                    return Shift.objects.filter(start_date__gte=first_day_of_month,end_date__lte=last_day_of_month,location=location_id,user=user)
        else:
            print("Inside all locations")
            if string == "day_by_area":
                today = timezone.now().date()      
                shifts = Shift.objects.filter(start_date=today)
                return shifts
            if string == "week_by_area":
                today = timezone.now().date()
                start_of_week = today - timezone.timedelta(days=today.weekday())
                end_of_week = start_of_week + timezone.timedelta(days=6)
                return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_week)
            if string == "two_weeks_by_area":
                today = timezone.now().date()
                start_of_week = today - timezone.timedelta(days=today.weekday())
                end_of_2_week = start_of_week + timezone.timedelta(days=13)
                return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_2_week)
            if string == "month_by_area":
                current_date = timezone.now().date()
                first_day_of_month = current_date.replace(day=1)
                last_day_of_month = first_day_of_month + timedelta(days=32 - first_day_of_month.day)
                last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
                return Shift.objects.filter(start_date__gte=first_day_of_month,end_date__lte=last_day_of_month)
            
            if string == "day_by_team_member":
                today = timezone.now().date()      
                shifts = Shift.objects.filter(start_date=today,user=user)
                return shifts
            if string == "week_by_team_member":
                today = timezone.now().date()
                start_of_week = today - timezone.timedelta(days=today.weekday())
                end_of_week = start_of_week + timezone.timedelta(days=6)
                return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_week,user=user)
            if string == "two_weeks_by_team_member":
                today = timezone.now().date()
                start_of_week = today - timezone.timedelta(days=today.weekday())
                end_of_2_week = start_of_week + timezone.timedelta(days=13)
                return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_2_week,user=user)
            if string == "four_weeks_by_team_member":
                today = timezone.now().date()
                start_of_week = today - timezone.timedelta(days=today.weekday())
                end_of_2_week = start_of_week + timezone.timedelta(days=27)
                return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_2_week,user=user)
            if string == "month_by_team_member":
                current_date = timezone.now().date()
                first_day_of_month = current_date.replace(day=1)
                last_day_of_month = first_day_of_month + timedelta(days=32 - first_day_of_month.day)
                last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
                return Shift.objects.filter(start_date__gte=first_day_of_month,end_date__lte=last_day_of_month,user=user)

class ShowSchedulesByDate(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    def get_queryset(self):
        start_date = self.request.GET.get('start_date', None)
        shifts = Shift.objects.filter(start_date=start_date)
        return shifts

class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    @transaction.atomic
    @action(methods=['patch'], detail=False)
    def bulk_update(self, request):
        data = {  # we need to separate out the id from the data
            i['id']: {k: v for k, v in i.items() if k != 'id'}
            for i in request.data
        }
        response = []
        for inst in self.get_queryset().filter(id__in=data.keys()):
            serializer = self.get_serializer(inst, data=data[inst.id], partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response.append(serializer.data)
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        location_id = self.request.GET.get('location_id', None)
        area_id = self.request.GET.get('area_id', None)
        if location_id:
            if area_id:
                shifts = Shift.objects.filter(location=location_id,area=area_id)
                shifts.delete()
                return Response("Shifts with specific Area are deleted")
            else:
                shifts = Shift.objects.filter(location=location_id)
                shifts.delete()
                return Response("Shifts with specific Location are deleted")
        else:
                all_shifts = Shift.objects.all()
                all_shifts.delete()
                return Response("All Shifts are deleted")

class RemoveEmptyShifts(APIView):
    def delete(self, request, shift_type=1):
        location_id = self.request.GET.get('location_id', None)
        area_id = self.request.GET.get('area_id', None)
        if location_id and area_id:
            shifts = Shift.objects.filter(shift_type=shift_type, location=location_id,area=area_id)
            shifts.delete()
            return Response("Empty Shifts with specific Area are removed",status=status.HTTP_204_NO_CONTENT)
        if location_id:
            shifts = Shift.objects.filter(shift_type=shift_type, location=location_id)
            shifts.delete()
            return Response("Empty Shifts with specific Location are removed",status=status.HTTP_204_NO_CONTENT)
        else:
            shifts = Shift.objects.filter(shift_type=shift_type)
            shifts.delete()
            return Response("Empty Shifts are removed",status=status.HTTP_204_NO_CONTENT)

class MarkEmptyShiftsAsOpen(APIView):
    def patch(self, request, shift_type=1):
        location_id = self.request.GET.get('location_id', None)
        area_id = self.request.GET.get('area_id', None)
        if location_id and area_id:
            shifts = Shift.objects.filter(shift_type=shift_type, location=location_id, area=area_id)
            for shift in shifts:
                shift.shift_type = 2
                shift.save()
            return Response("Empty shifts with specific Area are maked as Open Shifts")
        if location_id:
            shifts = Shift.objects.filter(shift_type=shift_type, location=location_id, area=area_id)
            for shift in shifts:
                shift.shift_type = 2
                shift.save()
            return Response("Empty shifts with specific Location are maked as Open Shifts")
        else:
            shifts = Shift.objects.all()
            for shift in shifts:
                shift.shift_type = 2
                shift.save()        
            return Response("Empty shifts are maked as Open Shifts")

class ShowStatsforShifts(APIView):
    def get(self, request):
        published_shifts = Shift.objects.filter(publish=True)
        unpublished_shifts = Shift.objects.filter(publish=False)
        Open_shift = Shift.objects.filter(shift_type=2)
        Empty_shift = Shift.objects.filter(shift_type=1)
        shift_stats = {
            "published_shifts" : len(published_shifts),
            "unpublished_shifts" : len(unpublished_shifts),
            "Open_shift" : len(Open_shift),
            "Empty_shift" : len(Empty_shift),
        }
        return Response({"shift_stats": shift_stats})

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

class PublishShift(APIView):
    def patch(self, request):
        shift_id = request.data.get('shift_id', None)
        publish = request.data.get('publish', None)
        shift = Shift.objects.filter(id=shift_id).first()
        if shift:
            if publish == True:
                shift.shift_type = publish  
                template = render_to_string('email_template.html')

                email_sent = send_mail(
                    'Your MaxPilot Shift details',
                    None,
                    settings.EMAIL_HOST_USER,
                    [shift.user.email],
                    fail_silently = False,
                    html_message = template
                )
                shift.save()
                return Response("Shift Published")
            else:
                return Response("Shift Unpublished, Change value of publish to True.")
        else:
            return Response(f"Object with ID {shift_id} does not exists.")
