import django_filters
from django import forms
from .models import process, posts, tasks, patterns
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

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
		self.filters['proc_category'].label="Kategoria"
	
	class Meta:
		model = process
		fields = ['proc_author', 'proc_assigned' ,'proc_category']



class UserTasksFilter(django_filters.FilterSet):
	task_proc=django_filters.CharFilter(field_name='tasks_proc__proc_process_name', lookup_expr='icontains', label='Proces')
	tasks_name=django_filters.CharFilter(field_name='tasks_name', lookup_expr='icontains', label='Tytuł')
	task_description=django_filters.CharFilter(field_name='tasks_description', lookup_expr='icontains', label='Tekst')

	task_start_date_year = django_filters.NumberFilter(field_name='tasks_start_date', lookup_expr='year', label='Rok')
	task_start_date_month = django_filters.NumberFilter(field_name='tasks_start_date', lookup_expr='month', label='Miesiąc')
	task_start_date_day = django_filters.NumberFilter(field_name='tasks_start_date', lookup_expr='day', label='Dzień')

	task_end_date_year = django_filters.NumberFilter(field_name='tasks_end_date', lookup_expr='year', label='Rok')
	task_end_date_month = django_filters.NumberFilter(field_name='tasks_end_date', lookup_expr='month', label='Miesiąc')
	task_end_date_day = django_filters.NumberFilter(field_name='tasks_end_date', lookup_expr='day', label='Dzień')
	

	def __init__(self, *args, **kwargs):
		super(UserTasksFilter, self).__init__(*args, **kwargs)

	class Meta:
		model = tasks
		fields = ['tasks_proc__proc_author','tasks_name', 'tasks_description']

#check in docs for users filter via queryset
	# @property
 #    def qs(self):
 #        parent = super().qs
 #        author = getattr(self.request, 'user', None)

 #        return parent.filter(is_published=True) \
 #            | parent.filter(author=author)

class UsersFilter(django_filters.FilterSet):
	user_first_name=django_filters.CharFilter(field_name='first_name', lookup_expr='icontains', label='Imię')
	user_last_name=django_filters.CharFilter(field_name='last_name', lookup_expr='icontains', label='Nazwisko')

	def __init__(self, *args, **kwargs):
		super(UsersFilter, self).__init__(*args, **kwargs)
		# at sturtup user doen't push Submit button, and QueryDict (in data) is empty
		if self.data == {}:
			self.queryset = self.queryset.none()

	class Meta:
		model = User
		fields = [ 'first_name', 'last_name']


class PatternFilter(django_filters.FilterSet):
	pat_author=django_filters.CharFilter(field_name='pat_author', lookup_expr='icontains', label='Autor')
	pat_name=django_filters.CharFilter(field_name='pat_name', lookup_expr='icontains', label='Nazwa')

	class Meta:
		model = patterns
		fields = [ 'pat_name', 'pat_author', 'pat_category']
