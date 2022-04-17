# Generated by Django 4.0.2 on 2022-04-17 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_worker'),
        ('requests', '0015_alter_requestcomment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.worker'),
        ),
    ]
