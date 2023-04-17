# Generated by Django 4.1.5 on 2023-03-31 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0009_location_location_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='area_location', to='business.location'),
        ),
        migrations.AlterField(
            model_name='location',
            name='business_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='business_location', to='business.business'),
        ),
        migrations.AlterField(
            model_name='operatinghours',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operating_hours_location', to='business.location'),
        ),
    ]
