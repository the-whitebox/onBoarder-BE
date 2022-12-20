# Generated by Django 4.1.3 on 2022-12-14 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employment', '0002_rename_friday_perdaypayrate_friday_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='workperiod',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userworkinghours',
            name='work_period',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employment.workperiod'),
        ),
    ]