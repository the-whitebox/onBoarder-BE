from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from deputy.models import DeputyBaseModel
from django.dispatch import receiver
from django.db.models.signals import pre_save

# Create your models here.
class UserProfile(DeputyBaseModel):

    NOT_SPECIFIED = "Not Specified"
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non Binary"
    GENDER_OPTIONS = (
        (NOT_SPECIFIED, 'Not Specified'), (MALE, 'Male'),
        (FEMALE, 'Female'),(NON_BINARY, 'Non Binary'),
    )

    THEY_THEM = "They/Them"
    SHE_HER = "She/Her"
    HE_HIM = "He/Him"
    CUSTOM = "Custom"
    PRONOUN_OPTIONS = (
        (NOT_SPECIFIED, 'Not Specified'), (THEY_THEM, 'They/Them'),
        (SHE_HER, 'She/Her'),(HE_HIM, 'He/Him'), (CUSTOM, "Custom")
    )


    profile_avatar = models.ImageField(upload_to='profile_avatars/', blank=True, null=True)

    display_name = models.CharField(_('full name'), max_length=150, blank=True)
    full_name = models.CharField(max_length=70, blank=True, null=True)

    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=70, blank=True, null=True)
    phone_number = models.CharField(null=True, blank=True, max_length=255)
    emergency_contact_name = models.CharField(null=True, blank=True, max_length=255)
    emergency_phone_number = models.CharField(null=True, blank=True, max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, blank=True,null=True, choices=GENDER_OPTIONS,default=NOT_SPECIFIED, help_text='Which gender does this user belong to')
    pronouns = models.CharField(max_length=255, blank=True,null=True, choices=PRONOUN_OPTIONS,default=NOT_SPECIFIED, help_text='Which pronoun does this user belong to')
    custom_pronoun = models.CharField(max_length=255, blank=True,null=True)

    def __str__(self):
        return str(self.user.email)


@receiver(pre_save, sender=UserProfile)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        existing_image = UserProfile.objects.get(pk=instance.pk)
        if instance.profile_avatar and existing_image.profile_avatar != instance.profile_avatar:
            existing_image.profile_avatar.delete(False)
    else:
        pass

class User(AbstractUser, DeputyBaseModel):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(_('email address'), null=True, blank=True)

    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    is_client = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'profile']

    def __str__(self):
        return "{}".format(self.username)

    def get_user_status(self):
        return 'Active' if self.is_active else 'Suspended'

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.profile_id:
            self.profile = UserProfile.objects.create()

        super(User, self).save(*args, **kwargs)


# class BusinessProfile(DeputyBaseModel):

#     HEALTHCARE = "Healthcare"
#     RETAIL_HOSPITALITY = "Retail & Hospitality"
#     SERVICES = "Services"
#     CHARITY = "Charity"
#     OTHER = "Other"
#     BUSINESS_TYPES = (
#         (HEALTHCARE, 'Healthcare'), (RETAIL_HOSPITALITY, 'Retail & Hospitality'),
#         (SERVICES, 'Services'),(CHARITY, 'Charity'), (OTHER, 'Other')
#     )

#     THEY_THEM = "Veterinary clinic"
#     SHE_HER = "Dental clinic"
#     HE_HIM = "Primary care physician"
#     CUSTOM = "Outpatient care centers"
#     CUSTOM = "Specialty clinics / Practitioners"
#     CUSTOM = "Care facility"
#     CUSTOM = "In-Home care"
#     CUSTOM = "Hospitals"
#     CUSTOM = "Pharmacies / Drug stores"

#     CUSTOM = "Fast food / Cashier restaurants"
#     CUSTOM = "Cafes / Coffee shops"
#     CUSTOM = "Sit down restaurants"
#     CUSTOM = "Pharmacies & drug stores"
#     CUSTOM = "Home, hardware & garden stores"
#     CUSTOM = "Clothing & personal care stores"
#     CUSTOM = "Bar / Club"
#     CUSTOM = "Food & beverage stores"
#     CUSTOM = "Auto, electronics & appliance stores"
#     CUSTOM = "Accommodation"
#     CUSTOM = "Catering"
#     CUSTOM = "Hospitality other"
#     CUSTOM = "Retail other"

#     CUSTOM = "Childcare Centers"
#     CUSTOM = "Security services"
#     CUSTOM = "Cleaning services"
#     CUSTOM = "Outpatient care centers"
#     CUSTOM = "Outpatient care centers"
#     CUSTOM = "Outpatient care centers"
#     INDUSTRY_TYPES = (
#         (NOT_SPECIFIED, 'Not Specified'), (THEY_THEM, 'They/Them'),
#         (SHE_HER, 'She/Her'),(HE_HIM, 'He/Him'), (CUSTOM, "Custom")
#     )


#     business_name = models.CharField(max_length=70, blank=True, null=True)
#     mobile_number = models.CharField(null=True, blank=True, max_length=255)
#     city = models.CharField(max_length=255, blank=True, null=True)
#     address = models.CharField(max_length=255, blank=True, null=True)
#     country = models.CharField(max_length=255, blank=True, null=True)
#     zip_code = models.CharField(max_length=255, blank=True, null=True)
#     email = models.EmailField(max_length=70, blank=True, null=True)
#     date_of_birth = models.DateField(null=True, blank=True)
#     gender = models.CharField(max_length=255, blank=True,null=True, choices=GENDER_OPTIONS,default=NOT_SPECIFIED, help_text='Which gender does this user belong to')
#     pronouns = models.CharField(max_length=255, blank=True,null=True, choices=PRONOUN_OPTIONS,default=NOT_SPECIFIED, help_text='Which pronoun does this user belong to')
#     custom_pronoun = models.CharField(max_length=255, blank=True,null=True)

#     def __str__(self):
#         return str(self.user.email)