# Generated by Django 3.0.8 on 2020-08-18 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info_flow', '0007_auto_20200814_1506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='files',
            name='files_is_private',
        ),
    ]
