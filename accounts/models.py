from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from deputy.models import DeputyBaseModel
from django.dispatch import receiver
from django.db.models.signals import pre_save

# Create your models here.
class UserProfile(DeputyBaseModel):
    profile_avatar = models.ImageField(upload_to='profile_avatars/', blank=True, null=True)

    display_name = models.CharField(_('full name'), max_length=150, blank=True)
    full_name = models.CharField(max_length=70, blank=True, null=True)

    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=70, blank=True, null=True)
    phone_number = models.CharField(null=True, blank=True, max_length=255)

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