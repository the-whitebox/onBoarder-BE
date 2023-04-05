from rest_framework import serializers
from employment.models import ( 
    UserWorkDetail, HourlyPayRate,
    HourlyOneAndHalfOvertimePayRate, SalaryPayRate,
    FixedPayRate, HourlyFortyFourHourOvertimePayRate,
    PerDayPayRate, UserPayDetail, 
    WorkPeriod, UserWorkingHours,
    UserLeaveEntitlements
    )


class UserWorkDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkDetail
        fields = (
            'id', 'works_at', 'hired_on', 'user'
            )

class HourlyPayRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourlyPayRate
        fields = (
            'id', 'weekday_rate', 'saturday_rate', 'sunday_rate', 'public_holiday_rate' 
            )

class HourlyOneAndHalfOvertimePayRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourlyOneAndHalfOvertimePayRate
        fields = (
            'id', 'hourly_rate', 'overtime_rate'
            )

class SalaryPayRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryPayRate
        fields = (
            'id', 'salary_period', 'salary_amount', 'salary_cost_allocation'
            )

class FixedPayRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedPayRate
        fields = (
            'id', 'base_fixed_rate'
            )

class HourlyFortyFourHourOvertimePayRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourlyFortyFourHourOvertimePayRate
        fields = (
            'id', 'base_hourly_rate', 'weekly_ot'
            )

class PerDayPayRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerDayPayRate
        fields = (
            'id', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'public_holidays'
            )

class UserPayDetailSerializer(serializers.ModelSerializer):
    hourly_pay_rate = HourlyPayRateSerializer(required=False)
    hourly_one_and_half_overtime_pay_rate = HourlyOneAndHalfOvertimePayRateSerializer(required=False)
    salary_pay_rate = SalaryPayRateSerializer(required=False)
    fixed_pay_rate = FixedPayRateSerializer(required=False)
    hourly_forty_four_hour_overtime_rate = HourlyFortyFourHourOvertimePayRateSerializer(required=False)
    per_day_pay_rate = PerDayPayRateSerializer(required=False)

    class Meta:
        model = UserPayDetail
        fields = (
            'id', 'employment_type', 'pay_rates', 'payroll_id', 'hourly_pay_rate', 'hourly_one_and_half_overtime_pay_rate', 
            'salary_pay_rate', 'fixed_pay_rate', 'hourly_forty_four_hour_overtime_rate', 'per_day_pay_rate', 'user'
            )
    
    def update(self, instance, validated_data):
        hourly_pay_rate_data = validated_data.pop('hourly_pay_rate')
        hourly_one_and_half_overtime_pay_rate_data = validated_data.pop('hourly_one_and_half_overtime_pay_rate')
        salary_pay_rate_data = validated_data.pop('salary_pay_rate')
        fixed_pay_rate_data = validated_data.pop('fixed_pay_rate')
        hourly_forty_four_hour_overtime_rate_data = validated_data.pop('hourly_forty_four_hour_overtime_rate')
        per_day_pay_rate_data = validated_data.pop('per_day_pay_rate')

        hourly_pay_rate = instance.hourly_pay_rate
        hourly_one_and_half_overtime_pay_rate= instance.hourly_one_and_half_overtime_pay_rate
        salary_pay_rate = instance.salary_pay_rate
        fixed_pay_rate = instance.fixed_pay_rate
        hourly_forty_four_hour_overtime_rate = instance.hourly_forty_four_hour_overtime_rate
        per_day_pay_rate = instance.per_day_pay_rate

        instance.employment_type = validated_data.get('employment_type', instance.employment_type)
        instance.pay_rates = validated_data.get('pay_rates', instance.pay_rates)
        instance.payroll_id = validated_data.get('payroll_id', instance.payroll_id)
        instance.save()

        if hourly_pay_rate_data:
            hourly_pay_rate.weekday_rate = hourly_pay_rate_data.get('weekday_rate', hourly_pay_rate.weekday_rate)
            hourly_pay_rate.saturday_rate = hourly_pay_rate_data.get('saturday_rate', hourly_pay_rate.saturday_rate)
            hourly_pay_rate.sunday_rate = hourly_pay_rate_data.get('sunday_rate', hourly_pay_rate.sunday_rate)
            hourly_pay_rate.public_holiday_rate = hourly_pay_rate_data.get('public_holiday_rate', hourly_pay_rate.public_holiday_rate)
            hourly_pay_rate.save()
        
        if hourly_one_and_half_overtime_pay_rate_data:
            hourly_one_and_half_overtime_pay_rate.hourly_rate = hourly_one_and_half_overtime_pay_rate_data.get('hourly_rate', hourly_one_and_half_overtime_pay_rate.hourly_rate)
            hourly_one_and_half_overtime_pay_rate.overtime_rate = hourly_one_and_half_overtime_pay_rate_data.get('overtime_rate', hourly_one_and_half_overtime_pay_rate.overtime_rate)
            hourly_one_and_half_overtime_pay_rate.save()
        
        if salary_pay_rate_data:
            salary_pay_rate.salary_period = salary_pay_rate_data.get('salary_period', salary_pay_rate.salary_period)
            salary_pay_rate.salary_amount = salary_pay_rate_data.get('salary_amount', salary_pay_rate.salary_amount)
            salary_pay_rate.salary_cost_allocation = salary_pay_rate_data.get('salary_cost_allocation', salary_pay_rate.salary_cost_allocation)
            salary_pay_rate.save()
        
        if fixed_pay_rate_data:
            fixed_pay_rate.base_fixed_rate = fixed_pay_rate_data.get('base_fixed_rate', fixed_pay_rate.base_fixed_rate)
            fixed_pay_rate.save()

        if hourly_forty_four_hour_overtime_rate_data:
            hourly_forty_four_hour_overtime_rate.base_hourly_rate = hourly_forty_four_hour_overtime_rate_data.get('base_hourly_rate', hourly_forty_four_hour_overtime_rate.base_hourly_rate)
            hourly_forty_four_hour_overtime_rate.weekly_ot = hourly_forty_four_hour_overtime_rate_data.get('weekly_ot', hourly_forty_four_hour_overtime_rate.weekly_ot)
            hourly_forty_four_hour_overtime_rate.save()

        if per_day_pay_rate_data:
            per_day_pay_rate.monday = per_day_pay_rate_data.get('monday', per_day_pay_rate.monday)
            per_day_pay_rate.tuesday = per_day_pay_rate_data.get('tuesday', per_day_pay_rate.tuesday)
            per_day_pay_rate.wednesday = per_day_pay_rate_data.get('wednesdayy', per_day_pay_rate.wednesday)
            per_day_pay_rate.thursday = per_day_pay_rate_data.get('thursday', per_day_pay_rate.thursday)
            per_day_pay_rate.friday = per_day_pay_rate_data.get('friday', per_day_pay_rate.friday)
            per_day_pay_rate.saturday = per_day_pay_rate_data.get('saturday', per_day_pay_rate.saturday)
            per_day_pay_rate.sunday = per_day_pay_rate_data.get('sunday', per_day_pay_rate.sunday)
            per_day_pay_rate.public_holidays = per_day_pay_rate_data.get('public_holidays', per_day_pay_rate.public_holidays)
            per_day_pay_rate.save()

        return instance

class WorkPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPeriod
        fields = (
            'id', 'work_period_length', 'next_work_period_day'
            )

class UserWorkingHoursSerializer(serializers.ModelSerializer):
    work_period = WorkPeriodSerializer(required=False)
    class Meta:
        model = UserWorkingHours
        fields = (
            'id', 'work_period', 'hours_per_work_period', 'total_hours_for_work_period', 'pay_overtime', 'stress_level', 'user'
            )
    def update(self, instance, validated_data):

        work_period_data = validated_data.pop('work_period')
        work_period = instance.work_period

        instance.hours_per_work_period = validated_data.get('hours_per_work_period', instance.hours_per_work_period)
        instance.total_hours_for_work_period = validated_data.get('total_hours_for_work_period', instance.total_hours_for_work_period)
        instance.pay_overtime = validated_data.get('pay_overtime', instance.pay_overtime)
        instance.stress_level = validated_data.get('stress_level', instance.stress_level)
        instance.save()

        # Update the attributes of the work_period model on the nested instance
        if work_period_data:
            work_period.work_period_length = work_period_data.get('work_period_length', work_period.work_period_length)
            work_period.next_work_period_day = work_period_data.get('next_work_period_day', work_period.next_work_period_day)
            work_period.save()
        
        return instance
    
    # def to_internal_value(self, data):
    #     self.fields['work_period'] = serializers.PrimaryKeyRelatedField(
    #         queryset=WorkPeriod.objects.all())
    #     return super(UserWorkingHoursSerializer, self).to_internal_value(data)

class UserLeaveEntitlementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLeaveEntitlements
        fields = (
            'id', 'leave_entitlement', 'user'
            )