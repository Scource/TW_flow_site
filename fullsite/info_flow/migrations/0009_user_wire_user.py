# Generated by Django 3.0.8 on 2022-05-31 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info_flow', '0008_auto_20220209_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='wire_user',
            field=models.IntegerField(null=True),
        ),
    ]
