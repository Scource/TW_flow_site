# Generated by Django 3.0.8 on 2020-08-29 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info_flow', '0017_auto_20200829_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='files_proc',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='info_flow.process'),
        ),
    ]