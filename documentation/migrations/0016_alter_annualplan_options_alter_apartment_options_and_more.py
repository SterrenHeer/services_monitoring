# Generated by Django 4.0.2 on 2022-05-06 07:53

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0006_alter_tenant_apartment_alter_worker_position'),
        ('documentation', '0015_alter_cleaningschedule_worker'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='annualplan',
            options={'verbose_name': 'годовой план', 'verbose_name_plural': 'Годовые планы'},
        ),
        migrations.AlterModelOptions(
            name='apartment',
            options={'verbose_name': 'квартиру', 'verbose_name_plural': 'Квартиры'},
        ),
        migrations.AlterModelOptions(
            name='building',
            options={'verbose_name': 'здание', 'verbose_name_plural': 'Здания'},
        ),
        migrations.AlterModelOptions(
            name='cleaningschedule',
            options={'verbose_name': 'график уборки', 'verbose_name_plural': 'Графики уборки'},
        ),
        migrations.AlterModelOptions(
            name='equipment',
            options={'verbose_name': 'оборудование', 'verbose_name_plural': 'Оборудование'},
        ),
        migrations.AlterModelOptions(
            name='position',
            options={'verbose_name': 'должность', 'verbose_name_plural': 'Должности'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'услугу', 'verbose_name_plural': 'Услуги'},
        ),
        migrations.AlterModelOptions(
            name='servicetype',
            options={'verbose_name': 'тип услуги', 'verbose_name_plural': 'Типы услуг'},
        ),
        migrations.AlterModelOptions(
            name='street',
            options={'verbose_name': 'улицу', 'verbose_name_plural': 'Улицы'},
        ),
        migrations.AlterField(
            model_name='annualplan',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documentation.building', verbose_name='Здание'),
        ),
        migrations.AlterField(
            model_name='annualplan',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Дата проведения'),
        ),
        migrations.AlterField(
            model_name='annualplan',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documentation.service', verbose_name='Услуга'),
        ),
        migrations.AlterField(
            model_name='annualplan',
            name='start_time',
            field=models.TimeField(default=datetime.time(8, 0), verbose_name='Время начала'),
        ),
        migrations.AlterField(
            model_name='annualplan',
            name='status',
            field=models.CharField(default='Запланирована', max_length=200, verbose_name='Состояние'),
        ),
        migrations.AlterField(
            model_name='annualplan',
            name='type',
            field=models.CharField(choices=[('Благоустройство', 'Благоустройство'), ('Ремонт', 'Ремонт')], default='Благоустройство', max_length=200, verbose_name='Характер'),
        ),
        migrations.AlterField(
            model_name='annualplan',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='annualplan',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.worker', verbose_name='Работник'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='apartment_number',
            field=models.IntegerField(verbose_name='Номер квартиры'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='area',
            field=models.IntegerField(verbose_name='Площадь помещения'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documentation.building', verbose_name='Здание'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='tenants_quantity',
            field=models.IntegerField(verbose_name='Количество жильцов'),
        ),
        migrations.AlterField(
            model_name='building',
            name='apartments_quantity',
            field=models.IntegerField(verbose_name='Количество квартир'),
        ),
        migrations.AlterField(
            model_name='building',
            name='number',
            field=models.IntegerField(verbose_name='Жилец'),
        ),
        migrations.AlterField(
            model_name='building',
            name='street',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documentation.street', verbose_name='Улица'),
        ),
        migrations.AlterField(
            model_name='cleaningschedule',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documentation.building', verbose_name='Здание'),
        ),
        migrations.AlterField(
            model_name='cleaningschedule',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Дата проведения'),
        ),
        migrations.AlterField(
            model_name='cleaningschedule',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documentation.service', verbose_name='Услуга'),
        ),
        migrations.AlterField(
            model_name='cleaningschedule',
            name='start_time',
            field=models.TimeField(default=datetime.time(8, 0), verbose_name='Время начала'),
        ),
        migrations.AlterField(
            model_name='cleaningschedule',
            name='status',
            field=models.CharField(default='Запланирована', max_length=200, verbose_name='Состояние'),
        ),
        migrations.AlterField(
            model_name='cleaningschedule',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='cleaningschedule',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.worker', verbose_name='Работник'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='position',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='position',
            name='service_type',
            field=models.ManyToManyField(to='documentation.ServiceType', verbose_name='Тип услуги'),
        ),
        migrations.AlterField(
            model_name='service',
            name='duration',
            field=models.TimeField(default=datetime.time(1, 0), verbose_name='Время исполнения'),
        ),
        migrations.AlterField(
            model_name='service',
            name='equipment',
            field=models.ManyToManyField(to='documentation.Equipment', verbose_name='Оборудование'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.IntegerField(verbose_name='Стоимость'),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documentation.servicetype', verbose_name='Тип услуги'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='nature',
            field=models.CharField(choices=[('Заявка', 'Заявка'), ('Замечание', 'Замечание'), ('Уборка', 'Уборка'), ('Ремонт', 'Ремонт'), ('Благоустройство', 'Благоустройство')], default='Замечание', max_length=20, verbose_name='Характер'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='street',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название улицы'),
        ),
    ]