# Generated by Django 4.0.2 on 2022-04-07 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0013_alter_requestcomment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestcomment',
            name='initial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='requests.requestcomment'),
        ),
    ]
