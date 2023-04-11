# Generated by Django 4.1.5 on 2023-04-07 05:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0016_shift_publish'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shift',
            old_name='date',
            new_name='end_date',
        ),
        migrations.AddField(
            model_name='shift',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]