# Generated by Django 4.0.2 on 2022-03-09 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0005_alter_street_name'),
        ('requests', '0003_requestcomment_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='documentation.building')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='documentation.service')),
            ],
        ),
    ]
