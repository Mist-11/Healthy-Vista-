# Generated by Django 4.1 on 2024-04-19 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_emailverifyrecord_send_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_time',
            field=models.DateTimeField(verbose_name='发送时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
