# Generated by Django 3.2.25 on 2024-04-12 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_identity'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(blank=True, choices=[('M', '男'), ('F', '女')], max_length=1, null=True),
        ),
    ]
