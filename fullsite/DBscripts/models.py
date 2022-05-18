from django.db import models
from django.conf import settings
from datetime import datetime
# Create your models here.


def report_path(instance, filename):
    date=datetime.now().strftime('%Y%m%d')
    report = instance.report_name
    return f'report_files/{date}/{report}'

class Report(models.Model):
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now_add=True)
    report_author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('2'), related_name='report_author')
    report_type = models.CharField(max_length=30)
    base_number = models.IntegerField()

class ReportItem(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    report_name = models.CharField(max_length=300)
    report_file = models.FileField(
        upload_to=report_path, blank=True, null=True)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now_add=True)

