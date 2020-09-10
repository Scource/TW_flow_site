import django_filters
from django import forms
from .models import process

class ProcessFilter(django_filters.FilterSet):
	proc_author=django_filters.CharFilter(lookup_expr='icontains')
	code=django_filters.CharFilter(lookup_expr='icontains')
	class Meta:
		model = process
		fields = ['proc_author', 'proc_process_name','proc_start_date']


class ConnFilter(django_filters.FilterSet):
	POB = forms.ModelChoiceField(queryset=UR_objects.objects.filter(name='qweqweq'), to_field_name = 'code')
	#POB = forms.ModelChoiceField(queryset=UR_objects.objects.filter(is_pob=0), to_field_name = 'name')
	SE = forms.ModelChoiceField(queryset=UR_objects.objects.filter(is_pob=1), to_field_name = 'name')
	class Meta:
		model = UR_conn
		fields = {'POB':['exact',],
		'DT_from': ['range'],
		}