# Generated by Django 4.1.5 on 2023-05-03 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_user_email_verified_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_verified_hash',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
