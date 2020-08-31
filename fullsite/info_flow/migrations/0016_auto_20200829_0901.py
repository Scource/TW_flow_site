# Generated by Django 3.0.8 on 2020-08-29 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info_flow', '0015_remove_files_files_tasks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='files',
            name='files_posts',
        ),
        migrations.AlterField(
            model_name='files',
            name='files_proc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='info_flow.process'),
        ),
    ]