# Generated by Django 3.0.8 on 2020-08-29 08:36

from django.db import migrations, models
import django.db.models.deletion
import info_flow.models


class Migration(migrations.Migration):

    dependencies = [
        ('info_flow', '0011_remove_messages_mess_file'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='process',
            options={'ordering': ['proc_created']},
        ),
        migrations.RemoveField(
            model_name='comments',
            name='com_file',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='post_file',
        ),
        migrations.RemoveField(
            model_name='tasks',
            name='tasks_file',
        ),
        migrations.AddField(
            model_name='files',
            name='files_posts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='info_flow.posts'),
        ),
        migrations.AddField(
            model_name='files',
            name='files_tasks',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='info_flow.tasks'),
        ),
        migrations.AlterField(
            model_name='files',
            name='files_document',
            field=models.FileField(upload_to=info_flow.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='files',
            name='files_proc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='info_flow.process'),
        ),
    ]
