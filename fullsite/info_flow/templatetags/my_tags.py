from django import template
from ..models import process, category
from django.db import models

register = template.Library()

@register.simple_tag
def create_process():
	cor_process=process(
		proc_author = user,
		proc_process_name = 'Korekta M+2',
		proc_description = 'Opis Korekta M+2',
		proc_created = models.DateTimeField(auto_now_add=True),
		proc_modified = models.DateTimeField(auto_now=True),
		proc_start_date = models.DateTimeField(auto_now_add=True),
		proc_end_date =models.DateTimeField(auto_now_add=True),
		proc_category = category.objects.get(pk=2),
		proc_is_active=True,
		proc_is_private=False,
		proc_is_deleted=False,
		proc_assigned = user)
	cor_process.save()