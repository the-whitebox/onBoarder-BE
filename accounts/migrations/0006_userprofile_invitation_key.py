# Generated by Django 4.1.3 on 2022-12-16 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_business'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='invitation_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
