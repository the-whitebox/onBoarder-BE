from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from accounts.models import User
from deputy.models import DeputyBaseModel

# Create your models here.
class UserWorkDetail(DeputyBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    works_at = models.CharField(max_length=255, null=True,blank=True)
    hired_on = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.user.email

class HourlyPayRate(DeputyBaseModel):
    weekday_rate = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    saturday_rate = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    sunday_rate = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    public_holiday_rate = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])

    def __int__(self):
        return self.id

class HourlyOneAndHalfOvertimePayRate(DeputyBaseModel):
    hourly_rate = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    overtime_rate = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])

    def __int__(self):
        return self.id

class SalaryPayRate(DeputyBaseModel):
    salary_period = models.PositiveIntegerField(null=True,blank=True)
    salary_amount = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    salary_cost_allocation = models.PositiveIntegerField(null=True,blank=True)

    def __int__(self):
        return self.id

class FixedPayRate(DeputyBaseModel):
    base_fixed_rate = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])

    def __int__(self):
        return self.id

class HourlyFortyFourHourOvertimePayRate(DeputyBaseModel):
    base_hourly_rate = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    weekly_ot = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])

    def __int__(self):
        return self.id

class PerDayPayRate(DeputyBaseModel):
    monday = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    tuesday = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    wednesday = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    thursday = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    Friday = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    saturday = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    sunday = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])
    public_holidays = models.DecimalField(max_digits=15,decimal_places=4,default=0,validators=[MinValueValidator(Decimal('0.01'))])

    def __int__(self):
        return self.id

class UserPayDetail(DeputyBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employment_type = models.PositiveIntegerField(null=True,blank=True)
    pay_rates = models.PositiveIntegerField(null=True,blank=True)
    payroll_id = models.CharField(max_length=255,null=True,blank=True)
    hourly_pay_rate = models.OneToOneField(HourlyPayRate, on_delete=models.CASCADE)
    hourly_one_and_half_overtime_pay_rate = models.OneToOneField(HourlyOneAndHalfOvertimePayRate, on_delete=models.CASCADE)
    salary_pay_rate = models.OneToOneField(SalaryPayRate, on_delete=models.CASCADE)
    fixed_pay_rate = models.OneToOneField(FixedPayRate, on_delete=models.CASCADE)
    hourly_forty_four_hour_overtime_rate = models.OneToOneField(HourlyFortyFourHourOvertimePayRate, on_delete=models.CASCADE)
    per_pay_rate = models.OneToOneField(PerDayPayRate, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

class WorkPeriod(DeputyBaseModel):
    work_period_length = models.PositiveIntegerField(null=True,blank=True)
    next_work_period_day = models.CharField(max_length=255,null=True,blank=True)

    def __int__(self):
        return self.id

class UserWorkingHours(DeputyBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    work_period = models.ForeignKey(WorkPeriod, on_delete=models.CASCADE)
    hours_per_work_period = models.PositiveIntegerField(null=True,blank=True)
    total_hours_for_work_period = models.TimeField(null=True,blank=True)
    pay_overtime = models.BooleanField(default=False)
    stress_level = models.PositiveIntegerField(null=True,blank=True)

    def __str__(self):
        return self.user.email

class UserLeaveEntitlements(DeputyBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    leave_entitlement = models.PositiveIntegerField(null=True,blank=True)

    def __str__(self):
        return self.user.email