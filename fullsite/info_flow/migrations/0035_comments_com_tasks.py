# Generated by Django 3.0.8 on 2020-10-06 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info_flow', '0034_auto_20201005_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='com_tasks',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='info_flow.tasks'),
            preserve_default=False,
        ),
    ]
