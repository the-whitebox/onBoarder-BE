from django.shortcuts import render
from accounts.models import User
from business.models import Business,Location,Area,OperatingHours,Shift,Template,Break
from business.serializers import BusinessSerializer,LocationSerializer,ShiftSerializer,TemplateSerializer
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
                    print(today)     
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

# Copy Shifts
import datetime
class ShiftCopyView(APIView):
    serializer_class = ShiftSerializer
    def post(self, request):
        location = self.request.GET.get('location')
        string = self.request.GET.get('string')
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')
        area_id = self.request.GET.get('area_id')

        today = datetime.date.today()
        previous_day = today - timedelta(days=1)
        next_day = today + timedelta(days=1)
        original_instance = Shift.objects.filter(location=location).first()
        if string == "copy to next day":
            copied_instance = Shift.objects.create(
                user = original_instance.user,
                area = original_instance.area,
                start = original_instance.start,
                finish = original_instance.finish,
                start_date = next_day,
                end_date = original_instance.end_date,
                publish = original_instance.publish,
                shift_type = original_instance.shift_type,
                location = original_instance.location
            )
            copied_instance.save()
            serializer = self.serializer_class(copied_instance)
            return Response(serializer.data)
        if string == "copy from previous day":
            print(original_instance.start_date)
            if original_instance.start_date == previous_day:
                copied_instance = Shift.objects.create(
                    user = original_instance.user,
                    area = original_instance.area,
                    start = original_instance.start,
                    finish = original_instance.finish,
                    start_date = today,
                    end_date = original_instance.end_date,
                    publish = original_instance.publish,
                    shift_type = original_instance.shift_type,
                    location = original_instance.location
                )
                copied_instance.save()
                serializer = self.serializer_class(copied_instance)
                return Response(serializer.data)
            
        if string == "Advanced":
            shifts = Shift.objects.filter(area=area_id,start_date=from_date)
            if shifts is not None:
                all_data = []
                for shift in shifts:
                    copied_instance = Shift.objects.create(
                        user = shift.user,
                        area = shift.area,
                        start = shift.start,
                        finish = shift.finish,
                        start_date = to_date,
                        end_date = shift.end_date,
                        publish = shift.publish,
                        shift_type = shift.shift_type,
                        location = shift.location
                    )
                    serializer = self.serializer_class(copied_instance)
                    all_data.append(serializer.data)
                return Response(all_data)
            else:
                return Response("No Shifts")
        else:
            return Response("Shifts not copied")
# Import Shifts
class ShiftImportView(APIView):
    serializer_class = ShiftSerializer
    def get(self, request):
        location = self.request.GET.get('location')
        string = self.request.GET.get('string')
        area = self.request.GET.get('area')
        date = self.request.GET.get('date')
        today = datetime.date.today()
        previous_day = today - timedelta(days=1)
        if string == "previous day":
            if area:
                imported_shifts = Shift.objects.filter(location=location,area=area,start_date=previous_day).first()
        if string == "choose date":
            if date:
                if area:
                    imported_shifts = Shift.objects.filter(location=location,area=area,start_date=date).first()
        serializer = self.serializer_class(imported_shifts)
        return Response(serializer.data)
    
# Save Tempplate
class SaveTemplate(APIView):
    def post(self,request):
        location_id = self.request.GET.get('location_id')
        name = request.data.get('name')
        today = datetime.date.today()
        description = request.data.get('description')
        if location_id:
            shifts = Shift.objects.filter(location=location_id)
        else:
            shifts = Shift.objects.all()
        if shifts:
            temp = Template.objects.create(name=name,description=description,date=today)
            temp.shifts.set(shifts)
            return Response("Template Created, all shifts has been copied")
        else:
            return Response("Please create shifts first")
        
# Load Template
class LoadTemplate(viewsets.ModelViewSet):
    serializer_class = TemplateSerializer
    def get_queryset(self):
        template_id = self.request.GET.get('template_id')
        if template_id:
            # shift_serializer_class = ShiftSerializer
            data = []
            queryset = Template.objects.filter(id=template_id)
            for data in queryset:
                shifts = data.shifts.all()
                print(shifts)
                for shift in shifts:
                    copied_instance = Shift.objects.create(
                    user = shift.user,
                    area = shift.area,
                    start = shift.start,
                    finish = shift.finish,
                    start_date = shift.start_date,
                    end_date = shift.end_date,
                    publish = shift.publish,
                    shift_type = shift.shift_type,
                    location = shift.location
                    )
                    print("sgift created", copied_instance.id)
                    data.shifts.add(copied_instance)
            return queryset
        else:
            queryset = Template.objects.all()
            return queryset
        
# Clone Shifts
class ShiftCloneView(APIView):
    serializer_class = ShiftSerializer
    def post(self, request):
        shift_id = self.request.GET.get('shift_id')
        no_of_shifts = int(self.request.GET.get('no_of_shifts'))
        original_instance = Shift.objects.filter(id=shift_id).first()
        all_data = []
        if original_instance:
            for shifts in range(no_of_shifts):
                copied_instance = Shift.objects.create(
                    user = original_instance.user,
                    area = original_instance.area,
                    start = original_instance.start,
                    finish = original_instance.finish,
                    start_date = original_instance.start_date,
                    end_date = original_instance.end_date,
                    publish = original_instance.publish,
                    shift_type = original_instance.shift_type,
                    location = original_instance.location
                )
                copied_instance.save()
                serializer = self.serializer_class(copied_instance)
                all_data.append(serializer.data)
                shifts = shifts + 1
        else:
            return Response("No shifts")
        return Response(all_data)
    
# download with Csv
import csv
from django.http import HttpResponse
class DownloadWithCsv(APIView):
    serializer_class = ShiftSerializer
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'
        writer = csv.writer(response)
        all_shifts = Shift.objects.all()
        writer.writerow(['location','user', 'area', 'start','finish', 'start_date', 'end_date','publish','shift_type'])
        for obj in all_shifts:
            writer.writerow([obj.location.location_name,obj.user, obj.area, obj.start,obj.finish,obj.start_date,obj.end_date,obj.publish,obj.shift_type])
        return response
    
# Send Offers api
class SendOffers(APIView):
    serializer_class = ShiftSerializer
    def patch(self, request):
        shift_id = request.data.get('shift_id', None)
        user_ids = request.data.get('users', None)
        shift = Shift.objects.get(id=shift_id)
        if shift:
            if user_ids:
                for user_id in user_ids:
                    user = User.objects.get(id=user_id)
                    shift.user = user
                    shift.shift_type = 2
                    email_sent = send_mail(
                        'Dupty',
                        'Your MaxPilot Shift details: you are invited for a shift',
                        settings.EMAIL_HOST_USER,
                        [shift.user.email],
                        fail_silently = False,
                    )
        else:
            return Response("Shift with provided ID does not Exists")
        shift.save()
        serializer = self.serializer_class(shift)
        return Response(serializer.data)

class ViewShiftHistory(APIView):
    def get(self,request):
        shift_id = int(self.request.GET.get('shift_id',None))
        print(shift_id)
        if shift_id:
            shift = Shift.objects.get(id=shift_id)
            return Response({
                "Created_by": shift.user.username,
                "Date" : shift.start_date
            })
        else:
            return Response("Please provide Shift ID")

# print by area
import io
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter,landscape
from reportlab.lib.units import inch

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

class PrintByArea(APIView):
    def get(self,request):
        string = self.request.GET.get("string")
        business_id = self.request.GET.get("business_id")
        business = Business.objects.filter(id=business_id).first()

        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)

        today = datetime.date.today()
        pdf.drawString(200, 750, "Schedule for "+ business.business_name)
        pdf.drawString(230, 730, str(today))

        PAGE_WIDTH, PAGE_HEIGHT = landscape(letter)
        LEFT_MARGIN = inch
        RIGHT_MARGIN = inch
        TOP_MARGIN = inch
        BOTTOM_MARGIN = inch
        usable_width = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN
        # usable_height = PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
        num_columns = 2.2
        column_widths = [usable_width / num_columns]
        locations = Location.objects.filter(business_location=business)
        print(locations)
        all_data = []
        # if string == "day_by_area":
        if locations:
            for location in locations:
                code = location.location_code
                areas = Area.objects.filter(location=location)
                for area in areas:
                    myarea = area.area_of_work
                    shifts = Shift.objects.filter(location=location,area=area)
                    for shift in shifts:
                        username = shift.user.username
                        start = shift.start
                        finish = shift.finish
                        breaks = Break.objects.filter(shift=shift)
                        for mybreak in breaks:
                            duration = mybreak.duration
                field = "[" + code + "]" + myarea
                shift_data = username + "\n" + str(start) + "-" + str(finish) + "\n" + str(duration) + " min break"
                data = [
                    ["",today],
                    [field,shift_data]
                    ]
            else:
                data = []
        table = Table(data,colWidths=column_widths)
        table.setStyle(TableStyle([
            # ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            # ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            # ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            # ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            # ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
    
        doc = SimpleDocTemplate('example.pdf', pagesize=landscape(letter),
                            leftMargin=LEFT_MARGIN, rightMargin=RIGHT_MARGIN,
                            topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN)
        doc.build([table])
        table.wrapOn(pdf, 10, 10)
        table.drawOn(pdf, 10, 640)

        pdf.showPage()
        pdf.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="example.pdf"'
        return response
