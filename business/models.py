from django.db import models
from MaxPilot.models import MaxPilotBaseModel
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone
# Create your models here.
class Business(MaxPilotBaseModel):
    business_name = models.CharField(max_length=70, blank=True, null=True)
    mobile_number = models.CharField(null=True, blank=True, max_length=255)
    business_type = models.PositiveIntegerField(null=True,blank=True)
    industry_type = models.PositiveIntegerField(null=True,blank=True)
    employees_range = models.PositiveIntegerField(null=True,blank=True)
    joining_purpose = models.PositiveIntegerField(null=True,blank=True)
    payroll_type = models.PositiveIntegerField(null=True,blank=True)
    pay_process_improvement_duration = models.PositiveIntegerField(null=True,blank=True)
    how_you_hear = models.PositiveIntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.business_name)

class Location(MaxPilotBaseModel):
    location_name = models.CharField(max_length=200)
    location_code = models.CharField(max_length=3, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.location_code = self.location_name[:3].upper()
        super(Location, self).save(*args, **kwargs)
    location_address = models.CharField(max_length=500, default=None)
    timezone = models.CharField(max_length=50, default='Asia/karachi')
    location_week_starts_on = models.PositiveIntegerField()    
    business_location = models.ForeignKey(Business,related_name='business_location', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.location_name)
    
class Area(MaxPilotBaseModel):
    physical_address = models.BooleanField(default=False,null=True,blank=True)
    area_of_work = models.CharField(max_length=50,null=True,blank=True)
    address = models.CharField(max_length=500,null=True,blank=True)
    location = models.ForeignKey(Location,related_name='areas', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.area_of_work

class OperatingHours(MaxPilotBaseModel):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"

    DAYS_OF_WEEK = (
        (Monday, 'Monday'),
        (Tuesday, 'Tuesday'),
        (Wednesday, 'Wednesday'),
        (Thursday, 'Thursday'),
        (Friday, 'Friday'),
        (Saturday, 'Saturday'),
        (Sunday, 'Sunday'),
    )
    days = models.CharField(max_length=9, choices=DAYS_OF_WEEK)
    start_time = models.TimeField(default='09:00')
    end_time = models.TimeField(default='05:00')
    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('End time must be after start time.')
    is_closed = models.BooleanField(default=False)
    location = models.ForeignKey(Location,related_name='operating_hours', on_delete=models.CASCADE)
    
class Shift(MaxPilotBaseModel):
    # Open = "Open"
    # Empty = "Empty"
    # shift_choices = (
    # (Open, 'Open'),
    # (Empty, 'Empty'),

    # )
    user = models.ForeignKey("accounts.User",on_delete=models.CASCADE)
    area = models.ForeignKey(Area,related_name='areas',on_delete=models.CASCADE)
    start = models.TimeField()
    finish = models.TimeField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    def clean(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError('End date cannot be before start date')
    publish = models.BooleanField(default=False)
    shift_type = models.PositiveIntegerField()
    location = models.ForeignKey(Location,related_name='shifts_location', on_delete=models.CASCADE)

class Break(MaxPilotBaseModel):
    break_type = models.CharField(max_length=100, default="Meal break")
    duration = models.TimeField(default="15")
    start = models.TimeField()
    finish = models.TimeField()
    shift = models.ForeignKey(Shift,related_name='shifts_break', on_delete=models.CASCADE, null=True, blank=True)

class Template(MaxPilotBaseModel):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(null=True,blank=True)
    date = models.DateField(default=timezone.now)
    shifts = models.ManyToManyField(Shift,related_name="shifts_template")
    def __str__(self):
        return self.name

# HEALTHCARE = "Healthcare"
    # RETAIL_HOSPITALITY = "Retail & Hospitality"
    # SERVICES = "Services"
    # CHARITY = "Charity"
    # OTHER = "Other"
    # BUSINESS_TYPES = (
    #     (HEALTHCARE, 'Healthcare'), (RETAIL_HOSPITALITY, 'Retail & Hospitality'),
    #     (SERVICES, 'Services'),(CHARITY, 'Charity'), (OTHER, 'Other')
    # )

    # VETERINARY_CLINIC = "Veterinary clinic"
    # DENTAL_CLINIC = "Dental clinic"
    # PRIMARY_CARE_PHYSICIAN = "Primary care physician"
    # OUTPATIENT_CARE_CENTERS = "Outpatient care centers"
    # SPECIALTY_CLINIC_PRACTITIONERS = "Specialty clinics / Practitioners"
    # CARE_FACILITY = "Care facility"
    # IN_HOME_CARE = "In-Home care"
    # HOSPITALS = "Hospitals"
    # PHARMACIES_OR_DRUG_STROES = "Pharmacies / Drug stores"

    # FAST_FOOD_CASHIER_RESTAURANTS = "Fast food / Cashier restaurants"
    # CAFES_COFFEE_SHOPS = "Cafes / Coffee shops"
    # SIT_DOWN_RESTAURANTS = "Sit down restaurants"
    # PHARMACIES_AND_DRUG_STROES = "Pharmacies & drug stores"
    # HOME_HARDWARE_GARDEN_STORES = "Home, hardware & garden stores"
    # CLOTHING_PERSONAL_CARE_STORES = "Clothing & personal care stores"
    # BAR_CLUB = "Bar / Club"
    # FOOD_BEVERAGE_STORES = "Food & beverage stores"
    # AUTO_ELECTRONICS_APPLIANCE_STORES = "Auto, electronics & appliance stores"
    # ACCOMMODATION = "Accommodation"
    # CATERING = "Catering"
    # HOSPITALITY_OTHER = "Hospitality other"
    # RETAIL_OTHER = "Retail other"

    # CHILDCARE_CENTERS = "Childcare Centers"
    # SECURITY_SERVICES = "Security services"
    # CLEANING_SERVICES = "Cleaning services"
    # CALL_CENTERS = "Call centers"
    # DELIVERY_POSTAL_SERVICES = "Delivery & postal services"
    # CRITICAL_EMERGENCY_SERVICES = "Critical & emergency services"
    # PROFESSIONAL_SERVICES = "Professional services"
    # PERSONAL_BEAUTY_SERVICES = "Personal & beauty services"
    # EMPLOYMENT_SERVICES = "Employment services"
    # SERVICES_OTHERS = "Services other"

    # ANIMAL_HEALTH = "Animal Health"
    # HEALTHCARE_OTHERS = "Healthcare Others"
    # CHILDCARE_COMMUNITY_CENTERS = "Childcare / Community centers"
    # ARTS_ENTERTAINMENT_RECREATION = "Arts, entertainment & recreation"
    # GOVERNMENT = "Government"
    # CLOTHING_PERSONAL_CARE_STORES = "Clothing & personal care stores"
    # OTHERS = "Others"

    # GYMS = "Gyms"
    # ARTS_ENTERTAINMENT_RECREATION = "Arts, entertainment & recreation"
    # CONSTRUCTION = "Construction"
    # EDUCATION = "Education"
    # MANUFACTURING = "Manufacturing"
    # TRANSPORTATION = "Transportation"
    # GOVERNMENT = "Government"
    # WAREHOUSING_STORAGE = "Warehousing & storage"
    # LOGISTICS_DISTRIBUTION_FREIGHT = "Logistics, distribution & freight"
    # ALL_OTHER = "All other"

    # INDUSTRY_TYPES = (
    #     (VETERINARY_CLINIC, "Veterinary clinic"),
    #     (DENTAL_CLINIC, "Dental clinic"),
    #     (PRIMARY_CARE_PHYSICIAN, "Primary care physician"),
    #     (OUTPATIENT_CARE_CENTERS, "Outpatient care centers"),
    #     (SPECIALTY_CLINIC_PRACTITIONERS, "Specialty clinics / Practitioners"),
    #     (CARE_FACILITY, "Care facility"),
    #     (IN_HOME_CARE, "In-Home care"),
    #     (HOSPITALS, "Hospitals"),
    #     (PHARMACIES_OR_DRUG_STROES, "Pharmacies / Drug stores"),
    
    #     (FAST_FOOD_CASHIER_RESTAURANTS, "Fast food / Cashier restaurants"),
    #     (CAFES_COFFEE_SHOPS, "Cafes / Coffee shops"),
    #     (SIT_DOWN_RESTAURANTS, "Sit down restaurants"),
    #     (PHARMACIES_AND_DRUG_STROES, "Pharmacies & drug stores"),
    #     (HOME_HARDWARE_GARDEN_STORES, "Home, hardware & garden stores"),
    #     (CLOTHING_PERSONAL_CARE_STORES, "Clothing & personal care stores"),
    #     (BAR_CLUB, "Bar / Club"),
    #     (FOOD_BEVERAGE_STORES, "Food & beverage stores"),
    #     (AUTO_ELECTRONICS_APPLIANCE_STORES, "Auto, electronics & appliance stores"),
    #     (ACCOMMODATION, "Accommodation"),
    #     (CATERING, "Catering"),
    #     (HOSPITALITY_OTHER, "Hospitality other"),
    #     (RETAIL_OTHER, "Retail other"),

    #     (CHILDCARE_CENTERS, "Childcare Centers"),
    #     (SECURITY_SERVICES, "Security services"),
    #     (CLEANING_SERVICES, "Cleaning services"),
    #     (CALL_CENTERS, "Call centers"),
    #     (DELIVERY_POSTAL_SERVICES, "Delivery & postal services"),
    #     (CRITICAL_EMERGENCY_SERVICES, "Critical & emergency services"),
    #     (PROFESSIONAL_SERVICES, "Professional services"),
    #     (PERSONAL_BEAUTY_SERVICES, "Personal & beauty services"),
    #     (EMPLOYMENT_SERVICES, "Employment services"),
    #     (SERVICES_OTHERS, "Services other"),

    #     (ANIMAL_HEALTH, "Animal Health"),
    #     (HEALTHCARE_OTHERS, "Healthcare Others"),
    #     (CHILDCARE_COMMUNITY_CENTERS, "Childcare / Community centers"),
    #     (ARTS_ENTERTAINMENT_RECREATION, "Arts, entertainment & recreation"),
    #     (GOVERNMENT, "Government"),
    #     (CLOTHING_PERSONAL_CARE_STORES, "Clothing & personal care stores"),
    #     (OTHERS, "Others"),

    #     (GYMS, "Gyms"),
    #     (ARTS_ENTERTAINMENT_RECREATION, "Arts, entertainment & recreation"),
    #     (CONSTRUCTION, "Construction"),
    #     (EDUCATION, "Education"),
    #     (MANUFACTURING, "Manufacturing"),
    #     (TRANSPORTATION, "Transportation"),
    #     (GOVERNMENT, "Government"),
    #     (WAREHOUSING_STORAGE, "Warehousing & storage"),
    #     (LOGISTICS_DISTRIBUTION_FREIGHT, "Logistics, distribution & freight"),
    #     (ALL_OTHER, "All other")

    # )

    # ONE_TO_FIFTEEN = "1-15"
    # SIXTEEN_TO_TWENTY_FIVE = "16-25"
    # TWENTY_SIX_TO_FORTY_NINE = "26-49"
    # FIFTY_TO_TWO_FORTY_NINE = "50-249"
    # TWO_FIFTY_TO_SEVEN_FORTY_NINE = "250-749"
    # SEVEN_FIFTY_PLUS = "750+"

    # EMPLOYEES_RANGE = (
    #     (ONE_TO_FIFTEEN, "1-15"), (SIXTEEN_TO_TWENTY_FIVE, "16-25"),
    #     (TWENTY_SIX_TO_FORTY_NINE, "26-49"), (FIFTY_TO_TWO_FORTY_NINE, "50-249"),
    #     (TWO_FIFTY_TO_SEVEN_FORTY_NINE, "250-749"), (SEVEN_FIFTY_PLUS, "750+")
    # )

    # SAVE_TIME_SCHEDULING = "Save time scheduling \n\nI want to know my teams availability, so I can create and share schedules"
    # TRACK_HOURS_WORKED = "Track hours worked \n\nI want a record of when my team works, so I can pay them correctly"
    # PROCESS_YOUR_TEAM_PAY = "Process your team’s pay \n\nI want to be able to process pay cycles without headaches"
    
    # PURPOSE_OF_JOINING = (
    #     (SAVE_TIME_SCHEDULING, "Save time scheduling \n\nI want to know my teams availability, so I can create and share schedules"),
    #     (TRACK_HOURS_WORKED, "Track hours worked \n\nI want a record of when my team works, so I can pay them correctly"),
    #     (PROCESS_YOUR_TEAM_PAY, "Process your team’s pay \n\nI want to be able to process pay cycles without headaches")
    # )

    # XERO = "xero"

    # PAYROLL_TYPES = (
    #     (XERO, "xero"),
    # )

    # ASAP = "As soon as possible"
    # IN_THE_NEAR_FUTURE = "In the near future"
    # JUST_LOOKING_AROUND = "Just looking around"

    # WHEN_IMPROVING_TEAM_PAY_PROCESS = (
    #     (ASAP, "As soon as possible"), (IN_THE_NEAR_FUTURE, "In the near future"),
    #     (JUST_LOOKING_AROUND, "Just looking around")
    # )

    # USED_MaxPilot_IN_THE_PAST = "Used MaxPilot in the past"
    # RECOMMENDED_FROM_A_FRIEND_OR_COLLEAGUE = "Recommended from a friend or colleague"
    # RECOMMENDED_FROM_A_BUSINESS_VENDOR = "Recommended from a business vendor"
    # READ_REVIEWS_OR_BLOG = "Read reviews or blog"
    # SAW_AN_AD_ABOUT_MaxPilot = "Saw an ad about MaxPilot"
    # SEARCHED_THE_INTERNET = "Searched the internet"
    # OTHER = "Other"

    # HOW_YOU_HEAR_ABOUT_US = (
    #     (USED_MaxPilot_IN_THE_PAST, "Used MaxPilot in the past"),
    #     (RECOMMENDED_FROM_A_FRIEND_OR_COLLEAGUE, "Recommended from a friend or colleague"),
    #     (RECOMMENDED_FROM_A_BUSINESS_VENDOR, "Recommended from a business vendor"),
    #     (READ_REVIEWS_OR_BLOG, "Read reviews or blog"),
    #     (SAW_AN_AD_ABOUT_MaxPilot, "Saw an ad about MaxPilot"),
    #     (SEARCHED_THE_INTERNET, "Searched the internet"),
    #     (OTHER, "Other")
    # )