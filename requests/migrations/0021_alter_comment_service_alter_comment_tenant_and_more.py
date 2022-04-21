# Generated by Django 4.0.2 on 2022-04-21 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0010_remove_equipment_cost_remove_equipment_quantity_and_more'),
        ('users', '0005_worker'),
        ('requests', '0020_comment_worker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='service',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='documentation.service'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='tenant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.tenant'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='request',
            name='service',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='documentation.service'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='request',
            name='tenant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.tenant'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='requestcomment',
            name='request',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='requests.request'),
            preserve_default=False,
        ),
    ]
