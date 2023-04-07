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
        print("this something")
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
                    print(related_obj.days)
                    related_obj.start_time = hours.start_time
                    print(related_obj.start_time)

                    related_obj.end_time = hours.end_time
                    related_obj.is_closed = hours.is_closed
                    related_obj.save()
            location.save()
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
        if location_id:
            queryset = User.objects.filter(user_location=location_id)
            return queryset
        else:
            all_location = Location.objects.all()
            print(all_location)
            all_users = []
            for location in all_location:
                people = User.objects.filter(user_location=location)
                for user in people:
                    all_users.append(user)
            return all_users


class ShowSchedules(viewsets.ModelViewSet):
    # queryset = Shift.objects.all()
    # serializer_class = ShiftSerializer

    # def get_queryset(self):
    #     location_id = self.request.GET.get('location_id', None)
    #     area = self.request.GET.get('area', None)
    #     try:
    #         my_location = Location.objects.get(id=location_id)
    #         my_area = Area.objects.filter(id=area).first()
    #         if my_location:
    #             if my_area:
    #                 shifts = Shift.objects.filter(location=my_location,area=my_area)
    #                 return shifts
    #             else:
    #                 shifts = Shift.objects.filter(location=my_location)
    #                 return shifts
    #     except:
    #             all_location = Location.objects.all()

    #             for location in all_location:
    #                 shifts = Shift.objects.filter(location=location)
    #                 return shifts

    queryset = Shift.objects.all()
    filter_backends = [filters.SearchFilter]
    serializer_class = ShiftSerializer

    def get_queryset(self):
        area_id = self.request.GET.get('area_id', None)
        team_member = self.request.GET.get('team_member', None)
        string = self.request.GET.get('string', None)
        location_id = self.request.GET.get('location_id', None)
        area_id = self.request.GET.get('area_id', None)
        if location_id:
            if area_id:
                if team_member:
                    print("Inside location_id,area_id,team members")
                    if string == "day":
                        today = timezone.now().date()      
                        shifts = Shift.objects.filter(start_date=today,location=location_id,area=area_id,user=team_member)
                        return shifts
                    if string == "week":
                        today = timezone.now().date()
                        start_of_week = today - timezone.timedelta(days=today.weekday())
                        end_of_week = start_of_week + timezone.timedelta(days=6)
                        return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_week,location=location_id,area=area_id,user=team_member)
                    if string == "two_weeks":
                        today = timezone.now().date()
                        start_of_week = today - timezone.timedelta(days=today.weekday())
                        end_of_2_week = start_of_week + timezone.timedelta(days=13)
                        return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_2_week,location=location_id,area=area_id,user=team_member)
                    if string == "four_weeks":
                        today = timezone.now().date()
                        start_of_week = today - timezone.timedelta(days=today.weekday())
                        end_of_2_week = start_of_week + timezone.timedelta(days=27)
                        return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_2_week,location=location_id,area=area_id,user=team_member)
                    if string == "month":
                        current_date = timezone.now().date()
                        first_day_of_month = current_date.replace(day=1)
                        last_day_of_month = first_day_of_month + timedelta(days=32 - first_day_of_month.day)
                        last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
                        return Shift.objects.filter(start_date__gte=first_day_of_month,end_date__lte=last_day_of_month,location=location_id,area=area_id,user=team_member)
                else:
                    print("Inside location_id,area_id")
                    if string == "day":
                        today = timezone.now().date()      
                        shifts = Shift.objects.filter(start_date=today,location=location_id,area=area_id)
                        return shifts
                    if string == "week":
                        today = timezone.now().date()
                        start_of_week = today - timezone.timedelta(days=today.weekday())
                        print(start_of_week)
                        end_of_week = start_of_week + timezone.timedelta(days=6)
                        return Shift.objects.filter(start_date__gte=start_of_week,end_date__gte=end_of_week,location=location_id,area=area_id)
                    if string == "two_weeks":
                        today = timezone.now().date()
                        start_of_week = today - timezone.timedelta(days=today.weekday())
                        end_of_2_week = start_of_week + timezone.timedelta(days=13)
                        return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_2_week,location=location_id,area=area_id)
                    if string == "month":
                        current_date = timezone.now().date()
                        first_day_of_month = current_date.replace(day=1)
                        last_day_of_month = first_day_of_month + timedelta(days=32 - first_day_of_month.day)
                        last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
                        return Shift.objects.filter(start_date__gte=first_day_of_month,end_date__lte=last_day_of_month,location=location_id,area=area_id)

            if team_member:
                print("Inside location_id,team members")
                
                if string == "day":
                    today = timezone.now().date()      
                    shifts = Shift.objects.filter(start_date=today,location=location_id,user=team_member)
                    return shifts
                if string == "week":
                    today = timezone.now().date()
                    start_of_week = today - timezone.timedelta(days=today.weekday())
                    end_of_week = start_of_week + timezone.timedelta(days=6)
                    return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_week,location=location_id,user=team_member)
                if string == "two_weeks":
                    today = timezone.now().date()
                    start_of_week = today - timezone.timedelta(days=today.weekday())
                    end_of_2_week = start_of_week + timezone.timedelta(days=13)
                    return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_2_week,location=location_id,user=team_member)
                if string == "four_weeks":
                    today = timezone.now().date()
                    start_of_week = today - timezone.timedelta(days=today.weekday())
                    end_of_2_week = start_of_week + timezone.timedelta(days=27)
                    return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_2_week,location=location_id,user=team_member)
                if string == "month":
                    current_date = timezone.now().date()
                    first_day_of_month = current_date.replace(day=1)
                    last_day_of_month = first_day_of_month + timedelta(days=32 - first_day_of_month.day)
                    last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
                    return Shift.objects.filter(start_date__gte=first_day_of_month,end_date__lte=last_day_of_month,location=location_id,user=team_member)

            else:
                print("Inside location_id")

                if string == "day":
                    today = timezone.now().date()      
                    shifts = Shift.objects.filter(start_date=today,location=location_id)
                    return shifts
                if string == "week":
                    today = timezone.now().date()
                    start_of_week = today - timezone.timedelta(days=today.weekday())
                    end_of_week = start_of_week + timezone.timedelta(days=6)
                    return Shift.objects.filter(start_date__gte=start_of_week,end_date__gte=end_of_week,location=location_id)
                if string == "two_weeks":
                    today = timezone.now().date()
                    start_of_week = today - timezone.timedelta(days=today.weekday())
                    end_of_2_week = start_of_week + timezone.timedelta(days=13)
                    return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_2_week,location=location_id)
                if string == "month":
                    current_date = timezone.now().date()
                    first_day_of_month = current_date.replace(day=1)
                    last_day_of_month = first_day_of_month + timedelta(days=32 - first_day_of_month.day)
                    last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
                    return Shift.objects.filter(start_date__gte=first_day_of_month,end_date__lte=last_day_of_month,location=location_id)

        else:
            print("Inside all locations")
            if string == "day":
                today = timezone.now().date()      
                shifts = Shift.objects.filter(start_date=today)
                return shifts
            if string == "week":
                today = timezone.now().date()
                start_of_week = today - timezone.timedelta(days=today.weekday())
                end_of_week = start_of_week + timezone.timedelta(days=6)
                return Shift.objects.filter(start_date__gte=start_of_week,end_date__gte=end_of_week)
            if string == "two_weeks":
                today = timezone.now().date()
                start_of_week = today - timezone.timedelta(days=today.weekday())
                end_of_2_week = start_of_week + timezone.timedelta(days=13)
                return Shift.objects.filter(start_date__gte=start_of_week,end_date__lte=end_of_2_week)
            if string == "month":
                current_date = timezone.now().date()
                first_day_of_month = current_date.replace(day=1)
                last_day_of_month = first_day_of_month + timedelta(days=32 - first_day_of_month.day)
                last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
                return Shift.objects.filter(start_date__gte=first_day_of_month,end_date__lte=last_day_of_month)



class ShowSchedulesByDate(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    def get_queryset(self):
        start_date = self.request.GET.get('start_date', None)
        shifts = Shift.objects.filter(start_date=start_date)
        return shifts

from rest_framework.decorators import action
class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer

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
        try:
            if location_id:
                if area_id:
                    shifts = Shift.objects.filter(location=location_id,area=area_id)
                    shifts.delete()
                    return Response("Shifts with specific Area are deleted")

                else:
                    shifts = Shift.objects.filter(location=location_id)
                    shifts.delete()
                    return Response("Shifts with specific Location are deleted")
        except:
                all_shifts = Shift.objects.all()
                all_shifts.delete()


class RemoveEmptyShifts(APIView):
    def delete(self, request, shift_type="Empty"):
        location_id = self.request.GET.get('location_id', None)
        area_id = self.request.GET.get('area_id', None)
        # my_location = Location.objects.get(id=location_id)
        # my_area = Area.objects.filter(id=area_id).first()
        if location_id and area_id:
            shifts = Shift.objects.filter(shift_type=shift_type, location=location_id,area=area_id)
            shifts.delete()
            return Response("Empty Shifts with specific Area are deleted",status=status.HTTP_204_NO_CONTENT)

        if location_id:
            shifts = Shift.objects.filter(shift_type=shift_type, location=location_id)
            shifts.delete()
            return Response("Empty Shifts with specific Location are deleted",status=status.HTTP_204_NO_CONTENT)
        
        else:
            shifts = Shift.objects.filter(shift_type=shift_type)
            shifts.delete()
            return Response("Empty Shifts with specific Location are deleted",status=status.HTTP_204_NO_CONTENT)


class MarkEmptyShiftsAsOpen(APIView):

    def patch(self, request, shift_type="Empty"):
        location_id = self.request.GET.get('location_id', None)
        area_id = self.request.GET.get('area_id', None)
        if location_id and area_id:
            shifts = Shift.objects.filter(shift_type=shift_type, location=location_id, area=area_id)
            for shift in shifts:
                shift.shift_type = "Open"
                shift.save()
            return Response("Empty shifts with specific Area are maked as Open Shifts")
        if location_id:
            shifts = Shift.objects.filter(shift_type=shift_type, location=location_id, area=area_id)
            for shift in shifts:
                shift.shift_type = "Open"
                shift.save()
            return Response("Empty shifts with specific Location are maked as Open Shifts")
        else:
            shifts = Shift.objects.all()
            for shift in shifts:
                shift.shift_type = "Open"
                shift.save()        
            return Response("Empty shifts are maked as Open Shifts")

class ShowStatsforShifts(APIView):
    def get(self, request):
        published_shifts = Shift.objects.filter(publish=True)
        unpublished_shifts = Shift.objects.filter(publish=False)
        Open_shift = Shift.objects.filter(shift_type="Open")
        Empty_shift = Shift.objects.filter(shift_type="Empty")

        shift_stats = {
            "published_shifts" : len(published_shifts),
            "unpublished_shifts" : len(unpublished_shifts),
            "Open_shift" : len(Open_shift),
            "Empty_shift" : len(Empty_shift),
        }
        return Response({"shift_stats": shift_stats})
    