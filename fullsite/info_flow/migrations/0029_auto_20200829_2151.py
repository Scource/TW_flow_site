# Generated by Django 3.0.8 on 2020-08-29 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info_flow', '0028_auto_20200829_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='proc_is_private',
            field=models.BooleanField(default=False),
        ),
    ]
