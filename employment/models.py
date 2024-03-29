from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from accounts.models import User
from MaxPilot.models import MaxPilotBaseModel

# Create your models here.
class UserWorkDetail(MaxPilotBaseModel):
    user = models.OneToOneField(User, related_name='work_detail', on_delete=models.CASCADE)
    works_at = models.CharField(max_length=255, null=True,blank=True)
    hired_on = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.user.email

class HourlyPayRate(MaxPilotBaseModel):
    weekday_rate = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    saturday_rate = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    sunday_rate = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    public_holiday_rate = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])

    def __int__(self):
        return self.id

class HourlyOneAndHalfOvertimePayRate(MaxPilotBaseModel):
    hourly_rate = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    overtime_rate = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])

    def __int__(self):
        return self.id

class SalaryPayRate(MaxPilotBaseModel):
    salary_period = models.PositiveIntegerField(null=True,blank=True)
    salary_amount = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    salary_cost_allocation = models.PositiveIntegerField(null=True,blank=True)

    def __int__(self):
        return self.id

class FixedPayRate(MaxPilotBaseModel):
    base_fixed_rate = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])

    def __int__(self):
        return self.id

class HourlyFortyFourHourOvertimePayRate(MaxPilotBaseModel):
    base_hourly_rate = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    weekly_ot = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])

    def __int__(self):
        return self.id

class PerDayPayRate(MaxPilotBaseModel):
    monday = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    tuesday = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    wednesday = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    thursday = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    friday = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    saturday = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    sunday = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    public_holidays = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])

    def __int__(self):
        return self.id

class UserPayDetail(MaxPilotBaseModel):
    user = models.OneToOneField(User, related_name='pay_detail', on_delete=models.CASCADE)
    employment_type = models.PositiveIntegerField(null=True,blank=True)
    pay_rates = models.PositiveIntegerField(null=True,blank=True)
    payroll_id = models.CharField(max_length=255,null=True,blank=True)
    hourly_pay_rate = models.OneToOneField(HourlyPayRate, related_name='hourly_pay_rate', on_delete=models.CASCADE)
    hourly_one_and_half_overtime_pay_rate = models.OneToOneField(HourlyOneAndHalfOvertimePayRate, related_name='hourly_one_and_half_overtime_pay_rate', on_delete=models.CASCADE)
    salary_pay_rate = models.OneToOneField(SalaryPayRate, related_name='salary_pay_rate', on_delete=models.CASCADE)
    fixed_pay_rate = models.OneToOneField(FixedPayRate, related_name='fixed_pay_rate', on_delete=models.CASCADE)
    hourly_forty_four_hour_overtime_rate = models.OneToOneField(HourlyFortyFourHourOvertimePayRate, related_name='hourly_forty_four_hour_overtime_rate', on_delete=models.CASCADE)
    per_day_pay_rate = models.OneToOneField(PerDayPayRate, related_name='per_day_pay_rate', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

class WorkPeriod(MaxPilotBaseModel):
    work_period_length = models.PositiveIntegerField(null=True,blank=True)
    next_work_period_day = models.CharField(max_length=255,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __int__(self):
        return self.id

class UserWorkingHours(MaxPilotBaseModel):
    user = models.OneToOneField(User, related_name='working_hours', on_delete=models.CASCADE)
    work_period = models.OneToOneField(WorkPeriod, on_delete=models.CASCADE, null=True, blank=True)
    hours_per_work_period = models.PositiveIntegerField(null=True,blank=True)
    total_hours_for_work_period = models.TimeField(null=True,blank=True)
    pay_overtime = models.BooleanField(default=False)
    stress_level = models.PositiveIntegerField(null=True,blank=True)

    def __str__(self):
        return self.user.email

class UserLeaveEntitlements(MaxPilotBaseModel):
    user = models.ForeignKey(User, related_name='leave_entitlements', on_delete=models.CASCADE)
    leave_entitlement = models.PositiveIntegerField(null=True,blank=True)

    def __str__(self):
        return self.user.email