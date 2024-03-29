# Generated by Django 4.1.5 on 2023-01-09 15:05

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FixedPayRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('base_fixed_rate', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HourlyFortyFourHourOvertimePayRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('base_hourly_rate', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('weekly_ot', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HourlyOneAndHalfOvertimePayRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('hourly_rate', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('overtime_rate', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HourlyPayRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('weekday_rate', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('saturday_rate', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('sunday_rate', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('public_holiday_rate', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PerDayPayRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('monday', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('tuesday', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('wednesday', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('thursday', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('friday', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('saturday', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('sunday', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('public_holidays', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SalaryPayRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('salary_period', models.PositiveIntegerField(blank=True, null=True)),
                ('salary_amount', models.DecimalField(decimal_places=4, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('salary_cost_allocation', models.PositiveIntegerField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('work_period_length', models.PositiveIntegerField(blank=True, null=True)),
                ('next_work_period_day', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserWorkingHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('hours_per_work_period', models.PositiveIntegerField(blank=True, null=True)),
                ('total_hours_for_work_period', models.TimeField(blank=True, null=True)),
                ('pay_overtime', models.BooleanField(default=False)),
                ('stress_level', models.PositiveIntegerField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='working_hours', to=settings.AUTH_USER_MODEL)),
                ('work_period', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employment.workperiod')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserWorkDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('works_at', models.CharField(blank=True, max_length=255, null=True)),
                ('hired_on', models.DateField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='work_detail', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserPayDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('employment_type', models.PositiveIntegerField(blank=True, null=True)),
                ('pay_rates', models.PositiveIntegerField(blank=True, null=True)),
                ('payroll_id', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('fixed_pay_rate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fixed_pay_rate', to='employment.fixedpayrate')),
                ('hourly_forty_four_hour_overtime_rate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hourly_forty_four_hour_overtime_rate', to='employment.hourlyfortyfourhourovertimepayrate')),
                ('hourly_one_and_half_overtime_pay_rate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hourly_one_and_half_overtime_pay_rate', to='employment.hourlyoneandhalfovertimepayrate')),
                ('hourly_pay_rate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hourly_pay_rate', to='employment.hourlypayrate')),
                ('per_day_pay_rate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='per_day_pay_rate', to='employment.perdaypayrate')),
                ('salary_pay_rate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='salary_pay_rate', to='employment.salarypayrate')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pay_detail', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserLeaveEntitlements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('leave_entitlement', models.PositiveIntegerField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_entitlements', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
