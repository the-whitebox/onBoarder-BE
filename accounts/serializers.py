from rest_framework import serializers
from rest_framework.fields import empty
from django.contrib.auth import get_user_model
from accounts.models import (
    UserProfile, ENUMS,
    Role
)
from employment.serializers import (
    UserWorkDetailSerializer, UserPayDetailSerializer,
    UserWorkingHoursSerializer, UserLeaveEntitlementsSerializer
)
from employment.models import (
    UserWorkDetail, UserPayDetail,
    UserWorkingHours, UserLeaveEntitlements,
    HourlyPayRate, HourlyOneAndHalfOvertimePayRate,
    SalaryPayRate, FixedPayRate, 
    HourlyFortyFourHourOvertimePayRate, PerDayPayRate,
    WorkPeriod
)
from custom_utilities.helpers import get_base64_image


User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    # relative_profile_avatar = serializers.SerializerMethodField(read_only=True)
    # encoded_profile_avatar = serializers.SerializerMethodField(read_only=True)
    user_name = serializers.CharField(required=False)
    # full_name = serializers.CharField(required=False)
    # full_name = serializers.SerializerMethodField(read_only=True)
    user_id = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_username(obj):
        return obj.user.username

    # @staticmethod
    # def get_full_name(obj):
    #     return obj.user.get_full_name()

    @staticmethod
    def get_user_id(obj):
        return obj.user.id

    # @staticmethod
    # def get_relative_profile_avatar(obj):
    #     if obj.profile_avatar:
    #         # return obj.profile_avatar.url
    #         return obj.profile_avatar

    # @staticmethod
    # def get_relative_path_profile_avatar(obj):
    #     if obj.profile_avatar:
    #         # return obj.profile_avatar.path
    #         return obj.profile_avatar

    # @staticmethod
    # def get_encoded_profile_avatar(obj):
    #     image_path = UserProfileSerializer.get_relative_path_profile_avatar(obj)
    #     return get_base64_image(image_path)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'display_name', 'state', 'city', 'address', 'country', 'zip_code', 'email', 'phone_number', 'emergency_contact_name', 'emergency_phone_number', 'username',
            'date_of_birth', 'gender', 'pronouns', 'custom_pronoun', 'user_name', 'full_name', 'user_id')

    def update(self, instance, validated_data):
        # instance.profile_avatar = validated_data.get('profile_avatar', instance.profile_avatar)
        instance.user.username = validated_data.get('user_name', instance.user.username)
        instance.display_name = validated_data.get('display_name', instance.display_name)
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.address = validated_data.get('address', instance.address)
        instance.zip_code = validated_data.get('zip_code', instance.zip_code)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.emergency_contact_name = validated_data.get('emergency_contact_name', instance.emergency_contact_name)
        instance.emergency_phone_number = validated_data.get('emergency_phone_number', instance.emergency_phone_number)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.pronouns = validated_data.get('pronouns', instance.pronouns)
        instance.custom_pronoun = validated_data.get('custom_pronoun', instance.custom_pronoun)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        instance.user.save()

        return instance

class UserListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        user_mapping = {user.id: user for user in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for user_id, data in data_mapping.items():
            user = user_mapping.get(user_id, None)
            if user:
                ret.append(self.child.update(user, data))

        # # Perform deletions.
        # for user_id, user in user_mapping.items():
        #     if user_id not in data_mapping:
        #         user.delete()

        return ret

class UserSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        if instance:
            setattr(self.Meta, 'depth', 1)
        else:
            setattr(self.Meta, 'depth', 0)
        super(UserSerializer, self).__init__(instance, data, **kwargs)

    profile = UserProfileSerializer(required=False)
    work_detail = UserWorkDetailSerializer(required=False)
    pay_detail = UserPayDetailSerializer(required=False)
    working_hours = UserWorkingHoursSerializer(required=False)
    leave_entitlements = UserLeaveEntitlementsSerializer(required=False)
    user_status = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        depth = 0
        model = User
        fields = (
            'id', 'url', 'first_name', 'last_name', 'is_superuser', 'role', 'business', 'password', 'username',
            'email', 'user_status', 'is_active', 'profile', 'work_detail', 'pay_detail', 'working_hours', 'leave_entitlements'
        )
        # read_only_fields = ('groups', )
        extra_kwargs = {
            'password': {'write_only': True,
                         'required': False}
        }

    @staticmethod
    def get_user_status(obj):
        return obj.get_user_status()

    def create(self, validated_data):
        profile_data = validated_data.pop('profile',)
        profile = UserProfile.objects.create(**profile_data)

        # work_detail_data = validated_data.pop('work_detail')
        # pay_detail_data = validated_data.pop('pay_detail')
        # working_hours_data = validated_data.pop('working_hours')
        # leave_entitlements_data = validated_data.pop('leave_entitlements')
        
        password = validated_data.pop('password', None)
        user = User(**validated_data, profile=profile)
        if password:
            user.set_password(password)
        if user.is_superuser:
            user.is_staff = True
        user.save()

        work_detail = UserWorkDetail.objects.create(user=user)
        hourly_pay_rate = HourlyPayRate.objects.create()
        hourly_one_and_half_overtime_pay_rate = HourlyOneAndHalfOvertimePayRate.objects.create()
        salary_pay_rate = SalaryPayRate.objects.create()
        fixed_pay_rate = FixedPayRate.objects.create()
        hourly_forty_four_hour_overtime_rate = HourlyFortyFourHourOvertimePayRate.objects.create()
        per_day_pay_rate = PerDayPayRate.objects.create()
        pay_detail = UserPayDetail.objects.create(user=user, hourly_pay_rate=hourly_pay_rate, hourly_one_and_half_overtime_pay_rate=hourly_one_and_half_overtime_pay_rate,
        salary_pay_rate=salary_pay_rate, fixed_pay_rate=fixed_pay_rate, hourly_forty_four_hour_overtime_rate=hourly_forty_four_hour_overtime_rate,
        per_day_pay_rate=per_day_pay_rate)
        work_period = WorkPeriod.objects.create(user=user)
        working_hours = UserWorkingHours.objects.create(work_period=work_period, user=user)
        leave_entitlements = UserLeaveEntitlements.objects.create(user=user)

        profile.save()

        return user
        
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        work_detail_data = validated_data.pop('work_detail', None)
        pay_detail_data = validated_data.pop('pay_detail', None)
        working_hours_data = validated_data.pop('working_hours', None)
        leave_entitlements_data = validated_data.pop('leave_entitlements', None)

        profile = instance.profile
        work_detail = instance.work_detail
        pay_detail = instance.pay_detail
        working_hours = instance.working_hours
        leave_entitlements = instance.leave_entitlements

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.role = validated_data.get('role', instance.role)
        instance.save()

        if profile_data:
            profile.display_name = profile_data.get('display_name', profile.display_name)
            profile.state = profile_data.get('state', profile.state)
            profile.country = profile_data.get('country', profile.country)
            profile.phone_number = profile_data.get('phone_number', profile.phone_number)
            profile.full_name = profile_data.get('full_name', profile.full_name)
            profile.email = profile_data.get('email', profile.email)
            profile.city = profile_data.get('city', profile.city)
            profile.address = profile_data.get('address', profile.address)
            profile.zip_code = profile_data.get('zip_code', profile.zip_code)
            profile.emergency_contact_name = profile_data.get('emergency_contact_name', profile.emergency_contact_name)
            profile.emergency_phone_number = profile_data.get('emergency_phone_number', profile.emergency_phone_number)
            profile.date_of_birth = profile_data.get('date_of_birth', profile.date_of_birth)
            profile.gender = profile_data.get('gender', profile.gender)
            profile.pronouns = profile_data.get('pronouns', profile.pronouns)
            profile.custom_pronoun = profile_data.get('custom_pronoun', profile.custom_pronoun)
            profile.save()
        
        if work_detail_data:
            work_detail.works_at = work_detail_data.get('works_at', work_detail.works_at)
            work_detail.hired_on = work_detail_data.get('hired_on', work_detail.hired_on)
            work_detail.save()
        
        if pay_detail_data:
            pay_detail.employment_type = pay_detail_data.get('employment_type', pay_detail.employment_type)
            pay_detail.pay_rates = pay_detail_data.get('pay_rates', pay_detail.pay_rates)
            pay_detail.payroll_id = pay_detail_data.get('payroll_id', pay_detail.payroll_id)

            # Update the attributes of the hourly_pay_rate model on the nested instance
            if pay_detail_data.get('hourly_pay_rate', None):
                pay_detail.hourly_pay_rate.weekday_rate = pay_detail_data.get('hourly_pay_rate', pay_detail.hourly_pay_rate.weekday_rate).get('weekday_rate', pay_detail.hourly_pay_rate.weekday_rate)
                pay_detail.hourly_pay_rate.saturday_rate = pay_detail_data.get('hourly_pay_rate', pay_detail.hourly_pay_rate.saturday_rate).get('saturday_rate', pay_detail.hourly_pay_rate.saturday_rate)
                pay_detail.hourly_pay_rate.sunday_rate = pay_detail_data.get('hourly_pay_rate', pay_detail.hourly_pay_rate.sunday_rate).get('sunday_rate', pay_detail.hourly_pay_rate.sunday_rate)
                pay_detail.hourly_pay_rate.public_holiday_rate = pay_detail_data.get('hourly_pay_rate', pay_detail.hourly_pay_rate.public_holiday_rate).get('public_holiday_rate', pay_detail.hourly_pay_rate.public_holiday_rate)
                pay_detail.hourly_pay_rate.save()
            
            # Update the attributes of the hourly_one_and_half_overtime_pay_rate model on the nested instance
            if pay_detail_data.get('hourly_one_and_half_overtime_pay_rate', None):
                pay_detail.hourly_one_and_half_overtime_pay_rate.hourly_rate = pay_detail_data.get('hourly_one_and_half_overtime_pay_rate', pay_detail.hourly_one_and_half_overtime_pay_rate.hourly_rate).get('hourly_rate', pay_detail.hourly_one_and_half_overtime_pay_rate.hourly_rate)
                pay_detail.hourly_one_and_half_overtime_pay_rate.overtime_rate = pay_detail_data.get('hourly_one_and_half_overtime_pay_rate', pay_detail.hourly_one_and_half_overtime_pay_rate.overtime_rate).get('overtime_rate', pay_detail.hourly_one_and_half_overtime_pay_rate.overtime_rate)
                pay_detail.hourly_one_and_half_overtime_pay_rate.save()

            # Update the attributes of the salary_pay_rate model on the nested instance
            if pay_detail_data.get('salary_pay_rate', None):
                pay_detail.salary_pay_rate.salary_period = pay_detail_data.get('salary_pay_rate', pay_detail.salary_pay_rate.salary_period).get('salary_period', pay_detail.salary_pay_rate.salary_period)
                pay_detail.salary_pay_rate.salary_amount = pay_detail_data.get('salary_pay_rate', pay_detail.salary_pay_rate.salary_amount).get('salary_amount', pay_detail.salary_pay_rate.salary_amount)
                pay_detail.salary_pay_rate.salary_cost_allocation = pay_detail_data.get('salary_pay_rate', pay_detail.salary_pay_rate.salary_cost_allocation).get('salary_cost_allocation', pay_detail.salary_pay_rate.salary_cost_allocation)
                pay_detail.salary_pay_rate.save()

            # Update the attributes of the fixed_pay_rate model on the nested instance
            if pay_detail_data.get('fixed_pay_rate', None):
                pay_detail.fixed_pay_rate.base_fixed_rate = pay_detail_data.get('fixed_pay_rate', pay_detail.fixed_pay_rate.base_fixed_rate).get('base_fixed_rate', pay_detail.fixed_pay_rate.base_fixed_rate)
                pay_detail.fixed_pay_rate.save()
            
            # Update the attributes of the hourly_forty_four_hour_overtime_rate model on the nested instance
            if pay_detail_data.get('hourly_forty_four_hour_overtime_rate', None):
                pay_detail.hourly_forty_four_hour_overtime_rate.base_hourly_rate = pay_detail_data.get('hourly_forty_four_hour_overtime_rate', pay_detail.hourly_forty_four_hour_overtime_rate.base_hourly_rate).get('base_hourly_rate', pay_detail.hourly_forty_four_hour_overtime_rate.base_hourly_rate)
                pay_detail.hourly_forty_four_hour_overtime_rate.weekly_ot = pay_detail_data.get('hourly_forty_four_hour_overtime_rate', pay_detail.hourly_forty_four_hour_overtime_rate.weekly_ot).get('weekly_ot', pay_detail.hourly_forty_four_hour_overtime_rate.weekly_ot)
                pay_detail.hourly_forty_four_hour_overtime_rate.save()

            # Update the attributes of the per_day_pay_rate model on the nested instance
            if pay_detail_data.get('per_day_pay_rate', None):
                pay_detail.per_day_pay_rate.monday = pay_detail_data.get('per_day_pay_rate', pay_detail.per_day_pay_rate.monday).get('monday', pay_detail.per_day_pay_rate.monday)
                pay_detail.per_day_pay_rate.tuesday = pay_detail_data.get('per_day_pay_rate', pay_detail.per_day_pay_rate.tuesday ).get('tuesday', pay_detail.per_day_pay_rate.tuesday)
                pay_detail.per_day_pay_rate.wednesday = pay_detail_data.get('per_day_pay_rate', pay_detail.per_day_pay_rate.wednesday).get('wednesday', pay_detail.per_day_pay_rate.wednesday)
                pay_detail.per_day_pay_rate.thursday = pay_detail_data.get('per_day_pay_rate', pay_detail.per_day_pay_rate.thursday).get('thursday', pay_detail.per_day_pay_rate.thursday)
                pay_detail.per_day_pay_rate.friday = pay_detail_data.get('per_day_pay_rate', pay_detail.per_day_pay_rate.friday).get('friday', pay_detail.per_day_pay_rate.friday)
                pay_detail.per_day_pay_rate.saturday = pay_detail_data.get('per_day_pay_rate', pay_detail.per_day_pay_rate.saturday).get('saturday', pay_detail.per_day_pay_rate.saturday)
                pay_detail.per_day_pay_rate.sunday = pay_detail_data.get('per_day_pay_rate', pay_detail.per_day_pay_rate.sunday).get('sunday', pay_detail.per_day_pay_rate.sunday)
                pay_detail.per_day_pay_rate.public_holidays = pay_detail_data.get('per_day_pay_rate', pay_detail.per_day_pay_rate.public_holidays).get('public_holidays', pay_detail.per_day_pay_rate.public_holidays)
                pay_detail.per_day_pay_rate.save()

            pay_detail.save()

        return instance
    
    def to_internal_value(self, data):
        self.fields['role'] = serializers.PrimaryKeyRelatedField(
            queryset=Role.objects.all())
        return super(UserSerializer, self).to_internal_value(data)

class ENUMSerializer(serializers.ModelSerializer):
    class Meta:
        model = ENUMS
        fields = (
            'id', 'name', 'reference_id', 'group'
            )