# Generated by Django 4.1.5 on 2023-03-29 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0006_rename_end_operatinghours_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operatinghours',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.location'),
        ),
    ]