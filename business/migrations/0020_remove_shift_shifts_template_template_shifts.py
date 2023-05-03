# Generated by Django 4.1.5 on 2023-05-03 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0019_template_shift_shifts_template'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift',
            name='shifts_template',
        ),
        migrations.AddField(
            model_name='template',
            name='shifts',
            field=models.ManyToManyField(related_name='shifts_template', to='business.shift'),
        ),
    ]
