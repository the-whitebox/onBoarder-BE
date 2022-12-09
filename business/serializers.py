from rest_framework import serializers
from business.models import Business
from accounts.serializers import UserSerializer

class BusinessSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = Business
        fields = (
            'id', 'business_name', 'mobile_number', 'business_type', 'industry_type', 'total_employees', 'joining_purpose', 
            'payroll_type', 'pay_proces_improvement_duration', 'how_you_hear', 'user'
            )