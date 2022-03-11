# Generated by Django 4.0.2 on 2022-03-11 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('requests', '0005_alter_comment_tenant_alter_repairrequest_tenant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repairrequest',
            name='tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.tenant'),
        ),
    ]
