from django.contrib import admin
from employment.models import (
    UserWorkDetail, UserPayDetail,
    UserWorkingHours, UserLeaveEntitlements,
    HourlyPayRate, HourlyOneAndHalfOvertimePayRate,
    SalaryPayRate, FixedPayRate, 
    HourlyFortyFourHourOvertimePayRate, PerDayPayRate,
    WorkPeriod
)

# Register your models here.
admin.site.register(UserWorkDetail)
admin.site.register(UserPayDetail)
admin.site.register(UserWorkingHours)
admin.site.register(UserLeaveEntitlements)
admin.site.register(HourlyPayRate)
admin.site.register(HourlyOneAndHalfOvertimePayRate)
admin.site.register(SalaryPayRate)
admin.site.register(FixedPayRate)
admin.site.register(HourlyFortyFourHourOvertimePayRate)
admin.site.register(PerDayPayRate)
admin.site.register(WorkPeriod)