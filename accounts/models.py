from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from MaxPilot.models import MaxPilotBaseModel
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from business.models import Business,Location


# Create your models here.

class Document(MaxPilotBaseModel):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class ENUMS(MaxPilotBaseModel):
    name = models.CharField(max_length=450, null=True,blank=True)
    reference_id = models.PositiveIntegerField(null=True, blank=True)
    group = models.CharField(max_length=255, null=True,blank=True)

    def __str__(self):
        return str(self.name)

class UserProfile(MaxPilotBaseModel):

    # NOT_SPECIFIED = "Not Specified"
    # MALE = "Male"
    # FEMALE = "Female"
    # NON_BINARY = "Non Binary"
    # GENDER_OPTIONS = (
    #     (NOT_SPECIFIED, 'Not Specified'), (MALE, 'Male'),
    #     (FEMALE, 'Female'),(NON_BINARY, 'Non Binary'),
    # )

    # THEY_THEM = "They/Them"
    # SHE_HER = "She/Her"
    # HE_HIM = "He/Him"
    # CUSTOM = "Custom"
    # PRONOUN_OPTIONS = (
    #     (NOT_SPECIFIED, 'Not Specified'), (THEY_THEM, 'They/Them'),
    #     (SHE_HER, 'She/Her'),(HE_HIM, 'He/Him'), (CUSTOM, "Custom")
    # )


    # profile_avatar = models.ImageField(upload_to='profile_avatars/', blank=True, null=True)
    profile_avatar = GenericRelation(Document, related_query_name='user_profile', blank=True, null=True)

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
    gender = models.PositiveIntegerField(null=True,blank=True)
    pronouns = models.PositiveIntegerField(null=True,blank=True)
    custom_pronoun = models.CharField(max_length=255, blank=True,null=True)
    invitation_key = models.CharField(max_length=255, blank=True,null=True)

    def __str__(self):
        return str(self.user.email)


# @receiver(pre_save, sender=UserProfile)
# def delete_old_image(sender, instance, *args, **kwargs):
#     if instance.pk:
#         existing_image = UserProfile.objects.get(pk=instance.pk)
#         if instance.profile_avatar and existing_image.profile_avatar != instance.profile_avatar:
#             existing_image.profile_avatar.delete(False)
#     else:
#         pass

class Role(MaxPilotBaseModel):

    SYSTEM_ADMINISTRATOR = "System Administrator"
    SUPERVISOR = "Supervisor"
    EMPLOYEE = "Employee"
    LOCATION_MANAGER = "Location Manager"
    ADVISOR = "Advisor"
    
    ROLE_CHOICES = (
        (SYSTEM_ADMINISTRATOR, 'System Administrator'),
        (SUPERVISOR, 'Supervisor'),
        (EMPLOYEE, 'Employee'),
        (LOCATION_MANAGER, 'Location Manager'),
        (ADVISOR, 'Advisor'),
    )

    role = models.CharField(max_length=255, choices=ROLE_CHOICES,help_text='Select a role for user')

    def __str__(self):
        return self.role

class User(AbstractUser, MaxPilotBaseModel):
    username = models.CharField(max_length=50, unique=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True,blank=True)
    business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True, blank=True)
    user_location = models.ForeignKey(Location,related_name='people', on_delete=models.SET_NULL, null=True, blank=True)
    email_verified_hash = models.CharField(max_length=200,null=True,blank=True)
    email_verified = models.BooleanField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'profile']
    
    def __str__(self):
        return "{}".format(self.username)

    def get_user_status(self):
        return 'Active' if self.is_active else 'Suspended'

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.profile_id:
            self.profile = UserProfile.objects.create()

        super(User, self).save(*args, **kwargs)