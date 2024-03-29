# Generated by Django 4.0.2 on 2022-05-06 07:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documentation', '0016_alter_annualplan_options_alter_apartment_options_and_more'),
        ('users', '0007_alter_tenant_options_alter_worker_options_and_more'),
        ('requests', '0026_alter_comment_completion_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'замечание', 'verbose_name_plural': 'Замечания'},
        ),
        migrations.AlterModelOptions(
            name='request',
            options={'verbose_name': 'заявку', 'verbose_name_plural': 'Заявки'},
        ),
        migrations.AlterModelOptions(
            name='requestcomment',
            options={'verbose_name': 'комментарий по заявке', 'verbose_name_plural': 'Комментарии по заявкам'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='answer',
            field=models.CharField(blank=True, max_length=85, null=True, verbose_name='Ответ'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='completion_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата выполнения'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documentation.service', verbose_name='Услуга'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(default='На рассмотрении', max_length=200, verbose_name='Состояние'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='submission_date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата подачи'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.tenant', verbose_name='Жилец'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=85, verbose_name='Текст замечания'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.worker', verbose_name='Работник'),
        ),
        migrations.AlterField(
            model_name='request',
            name='answer',
            field=models.CharField(blank=True, max_length=85, null=True, verbose_name='Ответ'),
        ),
        migrations.AlterField(
            model_name='request',
            name='completion_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата выполнения'),
        ),
        migrations.AlterField(
            model_name='request',
            name='end_time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Время завершения'),
        ),
        migrations.AlterField(
            model_name='request',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documentation.service', verbose_name='Услуга'),
        ),
        migrations.AlterField(
            model_name='request',
            name='start_time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Время начала'),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('На рассмотрении', 'На рассмотрении'), ('В обработке', 'В обработке'), ('Принята', 'Принята'), ('Отклонена', 'Отклонена'), ('Отложена', 'Отложена'), ('Выполнена', 'Выполнена')], default='На рассмотрении', max_length=200, verbose_name='Состояние'),
        ),
        migrations.AlterField(
            model_name='request',
            name='submission_date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата подачи'),
        ),
        migrations.AlterField(
            model_name='request',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.tenant', verbose_name='Жилец'),
        ),
        migrations.AlterField(
            model_name='request',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.worker', verbose_name='Работник'),
        ),
        migrations.AlterField(
            model_name='requestcomment',
            name='answer',
            field=models.CharField(blank=True, max_length=85, null=True, verbose_name='Ответ'),
        ),
        migrations.AlterField(
            model_name='requestcomment',
            name='initial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='requests.requestcomment', verbose_name='Исходный комментарий'),
        ),
        migrations.AlterField(
            model_name='requestcomment',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requests.request', verbose_name='Заявка'),
        ),
        migrations.AlterField(
            model_name='requestcomment',
            name='status',
            field=models.CharField(default='Ответ', max_length=200, verbose_name='Состояние'),
        ),
        migrations.AlterField(
            model_name='requestcomment',
            name='submission_date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата подачи'),
        ),
        migrations.AlterField(
            model_name='requestcomment',
            name='text',
            field=models.CharField(max_length=600, verbose_name='Текст замечания'),
        ),
        migrations.AlterField(
            model_name='requestcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.DeleteModel(
            name='Recommendation',
        ),
    ]
