# Generated by Django 4.0.2 on 2022-04-07 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0011_rename_comment_text_requestcomment_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_text',
            field=models.CharField(help_text='Введите комментарий', max_length=600),
        ),
        migrations.AlterField(
            model_name='requestcomment',
            name='text',
            field=models.CharField(help_text='Введите комментарий', max_length=600),
        ),
    ]
