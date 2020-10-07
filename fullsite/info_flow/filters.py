import django_filters
from django import forms
from .models import process, posts

class ProcessFilter(django_filters.FilterSet):
	proc_process_name=django_filters.CharFilter(field_name='proc_process_name', lookup_expr='icontains', label='Tytuł')

	proc_description=django_filters.CharFilter(field_name='proc_description', lookup_expr='icontains', label='Tekst')

	proc_start_date_year = django_filters.NumberFilter(field_name='proc_start_date', lookup_expr='year', label='Rok')
	proc_start_date_month = django_filters.NumberFilter(field_name='proc_start_date', lookup_expr='month', label='Miesiąc')
	proc_start_date_day = django_filters.NumberFilter(field_name='proc_start_date', lookup_expr='day', label='Dzień')

	proc_end_date_year = django_filters.NumberFilter(field_name='proc_end_date', lookup_expr='year', label='Rok')
	proc_end_date_month = django_filters.NumberFilter(field_name='proc_end_date', lookup_expr='month', label='Miesiąc')
	proc_end_date_day = django_filters.NumberFilter(field_name='proc_end_date', lookup_expr='day', label='Dzień')
	

	def __init__(self, *args, **kwargs):
		super(ProcessFilter, self).__init__(*args, **kwargs)
		self.filters['proc_author'].label="Autor"
		self.filters['proc_assigned'].label="Przypisane"
	
	class Meta:
		model = process
		fields = [ 'proc_assigned','proc_author']




class PostsFilter(django_filters.FilterSet):
	posts_title=django_filters.CharFilter(lookup_expr='icontains', label='Tytuł')
	
	def __init__(self, *args, **kwargs):
		super(PostsFilter, self).__init__(*args, **kwargs)
		self.filters['posts_author'].label="Autor"

	class Meta:
		model = posts
		fields = ['posts_author']


class UserProcessFilter(django_filters.FilterSet):
	proc_process_name=django_filters.CharFilter(field_name='proc_process_name', lookup_expr='icontains', label='Tytuł')
	proc_description=django_filters.CharFilter(field_name='proc_description', lookup_expr='icontains', label='Tekst')
	proc_description=django_filters.CharFilter(field_name='proc_is_private', label='Tekst')

	proc_start_date_year = django_filters.NumberFilter(field_name='proc_start_date', lookup_expr='year', label='Rok')
	proc_start_date_month = django_filters.NumberFilter(field_name='proc_start_date', lookup_expr='month', label='Miesiąc')
	proc_start_date_day = django_filters.NumberFilter(field_name='proc_start_date', lookup_expr='day', label='Dzień')

	proc_end_date_year = django_filters.NumberFilter(field_name='proc_end_date', lookup_expr='year', label='Rok')
	proc_end_date_month = django_filters.NumberFilter(field_name='proc_end_date', lookup_expr='month', label='Miesiąc')
	proc_end_date_day = django_filters.NumberFilter(field_name='proc_end_date', lookup_expr='day', label='Dzień')
	

	def __init__(self, *args, **kwargs):
		super(UserProcessFilter, self).__init__(*args, **kwargs)
		self.filters['proc_category'].label="Autor"

	
	class Meta:
		model = process
		fields = ['proc_category']
