# Generated by Django 4.1.3 on 2022-12-06 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='custom_pronoun',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='emergency_contact_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='emergency_phone_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('Not Specified', 'Not Specified'), ('Male', 'Male'), ('Female', 'Female'), ('Non Binary', 'Non Binary')], default='Not Specified', help_text='Which gender does this user belong to', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='pronouns',
            field=models.CharField(blank=True, choices=[('Not Specified', 'Not Specified'), ('They/Them', 'They/Them'), ('She/Her', 'She/Her'), ('He/Him', 'He/Him'), ('Custom', 'Custom')], default='Not Specified', help_text='Which pronoun does this user belong to', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
    ]
