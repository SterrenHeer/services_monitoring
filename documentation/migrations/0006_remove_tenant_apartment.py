# Generated by Django 4.0.2 on 2022-03-11 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0005_alter_street_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenant',
            name='apartment',
        ),
    ]