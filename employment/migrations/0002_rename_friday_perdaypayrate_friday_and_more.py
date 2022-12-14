# Generated by Django 4.1.3 on 2022-12-12 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='perdaypayrate',
            old_name='Friday',
            new_name='friday',
        ),
        migrations.RenameField(
            model_name='userpaydetail',
            old_name='per_pay_rate',
            new_name='per_day_pay_rate',
        ),
        migrations.AlterField(
            model_name='userleaveentitlements',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='leave_entitlements', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userpaydetail',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pay_detail', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userworkdetail',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='work_detail', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userworkinghours',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='working_hours', to=settings.AUTH_USER_MODEL),
        ),
    ]
