from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from accounts.models import (
    UserProfile, Role
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Creating initial users and profiles'

    def handle(self, *args, **options):
        if User.objects.count() == 0:

            system_administrator = Role.objects.create(role=Role.SYSTEM_ADMINISTRATOR)
            supervisor = Role.objects.create(role=Role.SUPERVISOR)
            employee = Role.objects.create(role=Role.EMPLOYEE)
            location_manager = Role.objects.create(role=Role.LOCATION_MANAGER)
            advisor = Role.objects.create(role=Role.ADVISOR)

            # Create first company user
            user_profile = UserProfile.objects.create()

            user = User.objects.create(email="user1@company1.com", username="company1_user_1", role=supervisor, first_name="company1",
                                       last_name="user1", profile=user_profile)
            user.set_password("user1234")
            user.save()
            self.stdout.write(self.style.SUCCESS('Successfully created company user 1'))

            # Create second company user
            user_profile = UserProfile.objects.create()

            user = User.objects.create(email="user2@company1.com", username="company1_user_2", role=location_manager, first_name="company1",
                                       last_name="user2", profile=user_profile)
            user.set_password("user1234")
            user.save()
            self.stdout.write(self.style.SUCCESS('Successfully created company user 2'))

            # Create a super User
            user_profile = UserProfile.objects.create()
            user = User.objects.create_user(email="admin1@admin.com", username="admin1", role=system_administrator, first_name="admin1",
                                            last_name="admin1", profile=user_profile, is_staff=True, is_superuser=True)
            user.set_password("admin1234")
            user.save()
            self.stdout.write(self.style.SUCCESS('Successfully created admin 1'))
        else:
            self.stdout.write(self.style.SUCCESS('New users creation not needed.'))