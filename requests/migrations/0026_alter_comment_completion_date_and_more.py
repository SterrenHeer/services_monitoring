# Generated by Django 4.0.2 on 2022-04-26 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0025_requestcomment_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='completion_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='completion_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]