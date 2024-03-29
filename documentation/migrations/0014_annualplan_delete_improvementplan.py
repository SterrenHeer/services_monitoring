# Generated by Django 4.0.2 on 2022-04-30 08:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0006_alter_tenant_apartment_alter_worker_position'),
        ('documentation', '0013_alter_improvementplan_worker'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnualPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('status', models.CharField(default='Запланирована', max_length=200)),
                ('start_time', models.TimeField(default=datetime.time(8, 0))),
                ('type', models.CharField(choices=[('Благоустройство', 'Благоустройство'), ('Ремонт', 'Ремонт')], default='Благоустройство', max_length=200)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documentation.building')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documentation.service')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('worker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.worker')),
            ],
        ),
        migrations.DeleteModel(
            name='ImprovementPlan',
        ),
    ]
