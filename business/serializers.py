from rest_framework import serializers
from business.models import Business,Location,Area
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
    




class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = (
            'physical_address', 'area_of_work', 'address',
            )
class LocationSerializer(serializers.ModelSerializer):

    area = AreaSerializer(many=True, required=False)
    people = UserSerializer(many=True, required=False)

    class Meta:
        depth = 0
        model = Location
        fields = (
            'location_name', 'location_address', 'timezone', 'location_week_starts_on','business_location', 'area','people'
            )

    def create(self, validated_data):
        print(validated_data)
        areas_data = validated_data.pop('area',None)
        users_data = validated_data.pop('people',None)
        location = Location.objects.create(**validated_data)
        print(location)
        for data in areas_data:
            area = Area.objects.create(location=location, **data)
            print(area)
        for people in users_data:
            print(people)
            users = User.objects.create(user_location=location, **people)
            
            print(users)
        return location
    
    
        # return response
    
        # serialize the objects
        # location_data =  LocationSerializer(location).data
        # area_data =  AreaSerializer(area).data
        # user_data =  UserSerializer(users).data

        # # Return the serialized data in a dictionary
        # return {
        #     'location_data': location_data,
        #     'area_data': area_data,
        #     'user_data': user_data,
        # }