# Generated by Django 4.1.5 on 2023-04-13 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0017_rename_date_shift_end_date_shift_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='shift_type',
            field=models.PositiveIntegerField(),
        ),
    ]
