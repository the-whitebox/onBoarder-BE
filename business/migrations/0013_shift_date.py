# Generated by Django 4.1.5 on 2023-04-06 06:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0012_alter_break_shift_alter_shift_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
