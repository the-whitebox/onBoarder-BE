from rest_framework import serializers
from business.models import Business,Location,Area,OperatingHours
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer

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
            'is_closed', 'days', 'start_time','end_time','location'
            )

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = (
            'physical_address', 'area_of_work', 'address',
            )
class LocationSerializer(serializers.ModelSerializer):

    area = AreaSerializer(many=True, required=False)
    people = UserSerializer(many=True, required=False)
    operating_hours = OperatingHourSerializer(required=False)

    class Meta:
        depth = 0
        model = Location
        fields = (
            'id','location_name', 'location_address', 'timezone', 'location_week_starts_on','business_location', 'area','people','operating_hours'
            )

    def create(self, validated_data):
        print(validated_data)
        areas_data = validated_data.pop('area',None)
        users_data = validated_data.pop('people',None)

        location = Location.objects.create(**validated_data)
        print(location)
        if areas_data:
            for data in areas_data:
                area = Area.objects.create(location=location, **data)
                print(area)
        if users_data:
            for people in users_data:
                print(people)
                users = User.objects.create(user_location=location, **people)
                print(users)
        week_days = ['monday','Tuesday','Wednesday','Thursday','Friday','Satureday','Sunday']
        for days in week_days:
            operating_hours = OperatingHours.objects.create(location=location,days=days)
            print(operating_hours)       
        print(operating_hours)
        location.save()
        return location
    
    def update(self, instance, validated_data):
        # areas_data = validated_data.pop('area',None)
        # users_data = validated_data.pop('people',None)
        operating_hours_data = validated_data.pop('operating_hours', None)

        # print(instance)
        # area = instance.area
        # users = instance.users
        operating_hours = instance.operating_hours

        # if areas_data:
        #     area = Area.objects.get_or_create(**areas_data)[0]
        #     instance.area = area
        # return super().update(instance, validated_data)

        if areas_data:
            area.physical_address = areas_data.get('physical_address', area.physical_address)
            area.area_of_work = areas_data.get('area_of_work', area.area_of_work)
            area.address = areas_data.get('address', area.address)
            area.save()
        if users_data:
            users.location_name = users_data.get('location_name', users.location_name)
            users.location_address = users_data.get('location_address', users.location_address)
            users.timezone = users_data.get('timezone', users.timezone)
            users.location_week_starts_on = users_data.get('location_week_starts_on', users.location_week_starts_on)
            users.save()
        if operating_hours_data:
            operating_hours.days = operating_hours_data.get('days', operating_hours.days)
            operating_hours.start = operating_hours_data.get('start_time', operating_hours.start)
            operating_hours.end = operating_hours_data.get('end_time', operating_hours.end)
            operating_hours.is_closed = operating_hours_data.get('is_closed', operating_hours.is_closed)
            operating_hours.save()