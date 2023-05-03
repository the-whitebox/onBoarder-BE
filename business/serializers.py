from rest_framework import serializers
from business.models import Business,Location,Area,OperatingHours,Shift,Break,Template
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer
from django.core.mail import send_mail
from django.conf import settings

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = (
            'id', 'business_name', 'mobile_number', 'business_type', 'industry_type', 'employees_range', 'joining_purpose', 
            'payroll_type', 'pay_process_improvement_duration', 'how_you_hear'
            )
        
    def create(self, validated_data):
        business = Business(**validated_data)
        business.save()
        try:
            user = User.objects.get(id=self.context.get('request', None).user.id if self.context.get('request', None) else 0)
            user.business = business
            user.save()
        except User.DoesNotExist:
            return Response({'error': 'user_not_found'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return business
    
class OperatingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatingHours
        fields = (
            'id','is_closed', 'days', 'start_time','end_time','location'
            )

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = (
            'id','physical_address', 'area_of_work', 'address', 'location'
            )
class LocationSerializer(serializers.ModelSerializer):
    areas = AreaSerializer(required=False,many=True)
    people = UserSerializer(required=False,many=True)
    operating_hours = OperatingHourSerializer(required=False,many=True)

    class Meta:
        model = Location
        fields = (
            'id','location_name','location_code', 'location_address', 'timezone', 'location_week_starts_on','business_location','areas','people','operating_hours'
            )

    def create(self, validated_data):
        areas_data = validated_data.pop('areas',None)
        users_data = validated_data.pop('people',None)
        location = Location.objects.create(**validated_data)
        if areas_data:
            for data in areas_data:
                area = Area.objects.create(location=location, **data)
        if users_data:
            for data in users_data:
                people = User.objects.create(user_location=location, **data)
                email_sent = send_mail(
                    'Dupty',
                    f"welcome to MaxPilot. You have been added as Team members with Email address: {people.email}",
                    settings.EMAIL_HOST_USER,
                    [people.email],
                    fail_silently = False,
                )
        week_days = ['monday','Tuesday','Wednesday','Thursday','Friday','Satureday','Sunday']
        for days in week_days:
            operating_hours = OperatingHours.objects.create(location=location,days=days)
        return location
    
    def update(self, instance, validated_data):
        areas_data = validated_data.pop('areas',None)
        users_data = validated_data.pop('people',None)
        operating_hours_data = validated_data.pop('operating_hours', None)

        area = instance.areas
        users = instance.people
        operating_hours = instance.operating_hours

        instance.location_name = validated_data.get('location_name', instance.location_name)
        instance.location_code = validated_data.get('location_code', instance.location_code)
        instance.location_address = validated_data.get('location_address', instance.location_address)
        instance.timezone = validated_data.get('timezone', instance.timezone)
        instance.location_week_starts_on = validated_data.get('location_week_starts_on', instance.location_week_starts_on)
        
        related_objects = area.all()
        for related_obj in related_objects:
            if areas_data:
                for areas in areas_data:
                    related_obj.physical_address = areas.get('physical_address', related_obj.physical_address)
                    related_obj.area_of_work = areas.get('area_of_work', related_obj.area_of_work)
                    related_obj.address = areas.get('address', related_obj.address)
                    related_obj.save()
        # if users_data:
        #     for userss in users_data:
        #         users.location_name = userss.get('location_name', users.location_name)
        #         users.location_address = userss.get('location_address', users.location_address)
        #         users.timezone = userss.get('timezone', users.timezone)
        #         users.location_week_starts_on = userss.get('location_week_starts_on', users.location_week_starts_on)
        #         users.save()
        related_objects = operating_hours.all()
        for related_obj in related_objects:
            if operating_hours_data:
                for operating_hour in operating_hours_data:
                    # related_obj.days = operating_hour.get('days', related_obj.days)
                    related_obj.start_time = operating_hour.get('start_time', related_obj.start_time)
                    related_obj.end_time = operating_hour.get('end_time', related_obj.end_time)
                    related_obj.is_closed = operating_hour.get('is_closed', related_obj.is_closed)
                    related_obj.save()
        return instance

class DuplicateSerializer(serializers.ModelSerializer):

    areas = AreaSerializer(required=False,many=True)
    people = UserSerializer(required=False,many=True)
    operating_hours = OperatingHourSerializer(required=False)

    class Meta:
        depth = 0
        model = Location
        fields = (
            'id','location_name','location_code', 'location_address', 'timezone', 'location_week_starts_on','business_location','areas','people','operating_hours'
            )

    def create(self, validated_data):
        areas_data = validated_data.pop('areas',None)
        users_data = validated_data.pop('people',None)

        location = Location.objects.create(**validated_data)
        if areas_data:
            for data in areas_data:
                area = Area.objects.create(location=location, **data)
        if users_data:
            for data in users_data:
                people = User.objects.create(user_location=location, **data)

        week_days = ['monday','Tuesday','Wednesday','Thursday','Friday','Satureday','Sunday']
        for days in week_days:
            operating_hours = OperatingHours.objects.create(location=location,days=days)
        return location

class BreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Break
        fields = (
            'id', 'break_type', 'duration', 'start','finish','shift'
            )
        
class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = (
            'id', 'name', 'description','shifts'
            )

class ShiftSerializer(serializers.ModelSerializer):
    shift_break = BreakSerializer(required=False,many=True)
    class Meta:
        model = Shift
        fields = (
            'id', 'user', 'area', 'start','finish','start_date','end_date','publish','shift_type','location','shift_break'
            )
    
    def create(self,validated_data):
        shift_break_data = validated_data.pop('shift_break',None)

        shift = Shift.objects.create(**validated_data)
        if shift_break_data:
            for data in shift_break_data:
                break_ = Break.objects.create(shift=shift, **data)

        return shift
    
    def update(self, instance, validated_data):
        shifts_break_data = validated_data.pop('shifts_break',None)
        shifts_break = instance.shifts_break
        instance.user = validated_data.get('user', instance.user)
        instance.area = validated_data.get('area', instance.area)
        instance.start = validated_data.get('start', instance.start)
        instance.finish = validated_data.get('finish', instance.finish)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.shift_type = validated_data.get('shift_type', instance.shift_type)
        instance.location = validated_data.get('location', instance.location)
        related_objects = shifts_break.all()
        for related_obj in related_objects:
            if shifts_break_data:
                for shifts_break in shifts_break_data:
                    related_obj.break_type = shifts_break.get('break_type', related_obj.break_type)
                    related_obj.duration = shifts_break.get('duration', related_obj.duration)
                    related_obj.start = shifts_break.get('start', related_obj.start)
                    related_obj.finish = shifts_break.get('finish', related_obj.finish)
                    related_obj.shift = shifts_break.get('shift', related_obj.shift)
                    related_obj.save()
        return instance