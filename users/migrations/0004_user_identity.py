# Generated by Django 3.2.18 on 2024-03-19 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_simplerecord_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='identity',
            field=models.CharField(default='用户', max_length=10, unique=True),
        ),
    ]
