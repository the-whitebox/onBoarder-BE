# Generated by Django 4.1.5 on 2023-05-08 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0021_template_date'),
        ('accounts', '0013_remove_user_business_user_business'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='business',
            field=models.ManyToManyField(blank=True, related_name='business_user', to='business.business'),
        ),
    ]
