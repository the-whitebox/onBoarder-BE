# Generated by Django 4.1.5 on 2023-05-03 12:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0020_remove_shift_shifts_template_template_shifts'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]