# Generated by Django 4.1.3 on 2022-12-07 02:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('business_name', models.CharField(blank=True, max_length=70, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=255, null=True)),
                ('business_type', models.CharField(blank=True, choices=[('Healthcare', 'Healthcare'), ('Retail & Hospitality', 'Retail & Hospitality'), ('Services', 'Services'), ('Charity', 'Charity'), ('Other', 'Other')], help_text='What best describes your business?', max_length=255, null=True)),
                ('industry_type', models.CharField(blank=True, choices=[('Veterinary clinic', 'Veterinary clinic'), ('Dental clinic', 'Dental clinic'), ('Primary care physician', 'Primary care physician'), ('Outpatient care centers', 'Outpatient care centers'), ('Specialty clinics / Practitioners', 'Specialty clinics / Practitioners'), ('Care facility', 'Care facility'), ('In-Home care', 'In-Home care'), ('Hospitals', 'Hospitals'), ('Pharmacies / Drug stores', 'Pharmacies / Drug stores'), ('Fast food / Cashier restaurants', 'Fast food / Cashier restaurants'), ('Cafes / Coffee shops', 'Cafes / Coffee shops'), ('Sit down restaurants', 'Sit down restaurants'), ('Pharmacies & drug stores', 'Pharmacies & drug stores'), ('Home, hardware & garden stores', 'Home, hardware & garden stores'), ('Clothing & personal care stores', 'Clothing & personal care stores'), ('Bar / Club', 'Bar / Club'), ('Food & beverage stores', 'Food & beverage stores'), ('Auto, electronics & appliance stores', 'Auto, electronics & appliance stores'), ('Accommodation', 'Accommodation'), ('Catering', 'Catering'), ('Hospitality other', 'Hospitality other'), ('Retail other', 'Retail other'), ('Childcare Centers', 'Childcare Centers'), ('Security services', 'Security services'), ('Cleaning services', 'Cleaning services'), ('Call centers', 'Call centers'), ('Delivery & postal services', 'Delivery & postal services'), ('Critical & emergency services', 'Critical & emergency services'), ('Professional services', 'Professional services'), ('Personal & beauty services', 'Personal & beauty services'), ('Employment services', 'Employment services'), ('Services other', 'Services other'), ('Animal Health', 'Animal Health'), ('Healthcare Others', 'Healthcare Others'), ('Childcare / Community centers', 'Childcare / Community centers'), ('Arts, entertainment & recreation', 'Arts, entertainment & recreation'), ('Government', 'Government'), ('Clothing & personal care stores', 'Clothing & personal care stores'), ('Others', 'Others'), ('Gyms', 'Gyms'), ('Arts, entertainment & recreation', 'Arts, entertainment & recreation'), ('Construction', 'Construction'), ('Education', 'Education'), ('Manufacturing', 'Manufacturing'), ('Transportation', 'Transportation'), ('Government', 'Government'), ('Warehousing & storage', 'Warehousing & storage'), ('Logistics, distribution & freight', 'Logistics, distribution & freight'), ('All other', 'All other')], help_text='In which industry your business falls?', max_length=255, null=True)),
                ('total_employees', models.CharField(blank=True, choices=[('1-15', '1-15'), ('16-25', '16-25'), ('26-49', '26-49'), ('50-249', '50-249'), ('250-749', '250-749'), ('750+', '750+')], help_text='How many employees do you need to manage?', max_length=255, null=True)),
                ('joining_purpose', models.CharField(blank=True, choices=[('Save time scheduling \n\nI want to know my teams availability, so I can create and share schedules', 'Save time scheduling \n\nI want to know my teams availability, so I can create and share schedules'), ('Track hours worked \n\nI want a record of when my team works, so I can pay them correctly', 'Track hours worked \n\nI want a record of when my team works, so I can pay them correctly'), ('Process your team’s pay \n\nI want to be able to process pay cycles without headaches', 'Process your team’s pay \n\nI want to be able to process pay cycles without headaches')], help_text='What is the purpose of joining?', max_length=255, null=True)),
                ('payroll_type', models.CharField(blank=True, choices=[('xero', 'xero')], help_text='What payroll provider do you use?', max_length=255, null=True)),
                ('pay_proces_improvement_duration', models.CharField(blank=True, choices=[('As soon as possible', 'As soon as possible'), ('In the near future', 'In the near future'), ('Just looking around', 'Just looking around')], help_text='When are you looking to improve the way you process your team’s pay?', max_length=255, null=True)),
                ('how_you_hear', models.CharField(blank=True, choices=[('Used Deputy in the past', 'Used Deputy in the past'), ('Recommended from a friend or colleague', 'Recommended from a friend or colleague'), ('Recommended from a business vendor', 'Recommended from a business vendor'), ('Read reviews or blog', 'Read reviews or blog'), ('Saw an ad about Deputy', 'Saw an ad about Deputy'), ('Searched the internet', 'Searched the internet'), ('Other', 'Other')], help_text='How did you hear about', max_length=255, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
