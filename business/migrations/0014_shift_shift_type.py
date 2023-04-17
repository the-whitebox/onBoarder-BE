# Generated by Django 4.1.5 on 2023-04-06 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0013_shift_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='Shift_type',
            field=models.CharField(blank=True, choices=[('OPEN', 'OPEN'), ('EMPTY', 'EMPTY')], max_length=5, null=True),
        ),
    ]
