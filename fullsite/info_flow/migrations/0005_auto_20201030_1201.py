# Generated by Django 3.0.8 on 2020-10-30 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info_flow', '0004_patterns_patterns_elements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patterns_elements',
            name='pele_proc',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]