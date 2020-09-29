import django_filters
from django import forms
from .models import process, posts

class ProcessFilter(django_filters.FilterSet):
	proc_process_name=django_filters.CharFilter(lookup_expr='icontains', label='Tytuł')
	
	def __init__(self, *args, **kwargs):
		super(ProcessFilter, self).__init__(*args, **kwargs)
		self.filters['proc_author'].label="Autor"
		self.filters['proc_is_active'].label="Aktywne"
		self.filters['proc_assigned'].label="Przypisane"
	
	class Meta:
		model = process
		fields = ['proc_author', 'proc_is_active', 'proc_assigned']


class PostsFilter(django_filters.FilterSet):
	posts_title=django_filters.CharFilter(lookup_expr='icontains', label='Tytuł')
	
	def __init__(self, *args, **kwargs):
		super(PostsFilter, self).__init__(*args, **kwargs)
		self.filters['posts_author'].label="Autor"

	class Meta:
		model = posts
		fields = ['posts_author']

