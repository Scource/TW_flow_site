# Generated by Django 3.0.8 on 2020-08-29 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info_flow', '0014_remove_files_files_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='files',
            name='files_tasks',
        ),
    ]
