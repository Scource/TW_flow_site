# Generated by Django 3.0.8 on 2020-08-19 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info_flow', '0010_auto_20200819_1208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='mess_file',
        ),
    ]
