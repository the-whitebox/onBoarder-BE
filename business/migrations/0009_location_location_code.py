# Generated by Django 4.1.5 on 2023-03-30 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0008_alter_operatinghours_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='location_code',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]