import django_filters
from django import forms
from .models import process, posts

class ProcessFilter(django_filters.FilterSet):
	proc_process_name=django_filters.CharFilter(lookup_expr='icontains')
	proc_start_date_year = django_filters.NumberFilter(field_name='proc_start_date', lookup_expr='year')

	
	class Meta:
		model = process
		fields = ['proc_author','proc_start_date', 'proc_is_active']


class PostsFilter(django_filters.FilterSet):
	posts_title=django_filters.CharFilter(lookup_expr='icontains')
		
	class Meta:
		model = posts
		fields = ['posts_author']

