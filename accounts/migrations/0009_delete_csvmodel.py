# Generated by Django 4.1.5 on 2023-01-09 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_rename_file_csvmodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CSVModel',
        ),
    ]