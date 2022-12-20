# Generated by Django 4.1.3 on 2022-12-09 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_business_delete_businessprofile'),
        ('accounts', '0003_alter_enums_reference_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='business',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='business.business'),
        ),
    ]
