# Generated by Django 3.0.8 on 2020-08-18 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info_flow', '0008_remove_files_files_is_private'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='proc_file',
        ),
        migrations.AddField(
            model_name='files',
            name='files_proc',
            field=models.ForeignKey(default=30, on_delete=django.db.models.deletion.CASCADE, to='info_flow.process'),
            preserve_default=False,
        ),
    ]
