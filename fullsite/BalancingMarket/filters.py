import django_filters
from django import forms
from .models import Element, Connection, Powerplant


class ElementFilter(django_filters.FilterSet):
	CHOICES = ((None, '-----------'), (False, 'Nieuzupełniona'),
	           (True, 'Uzupełniona'))

	name = django_filters.CharFilter(
		field_name='name', lookup_expr='icontains')
	code = django_filters.CharFilter(
            field_name='code', lookup_expr='icontains')
	is_added = django_filters.BooleanFilter(field_name='is_added',
    	widget=forms.Select(attrs={'class': 'form-control'}, choices=CHOICES))
	
	class Meta:
		model = Element
		fields = ['name', 'code', 'is_added']


class ConnectionFilter(django_filters.FilterSet):
	POB = django_filters.CharFilter(
		field_name='POB__code', lookup_expr='icontains')
	SE = django_filters.CharFilter(
            field_name='SE__code', lookup_expr='icontains')
	
	class Meta:
		model = Connection
		fields = ['POB', 'SE']


class PowerplantFilter(django_filters.FilterSet):
	CHOICES = ((None, '-----------'), (False, 'Nieuzupełniona'),
            (True, 'Uzupełniona'))

	name = django_filters.CharFilter(
		field_name='name', lookup_expr='icontains')
	PPE = django_filters.CharFilter(
            field_name='PPE', lookup_expr='icontains')
	cspr_id = django_filters.NumberFilter(
            field_name='cspr_id')
	is_added = django_filters.BooleanFilter(field_name='is_added',
        widget=forms.Select(attrs={'class': 'form-control'}, choices=CHOICES))
	class Meta:
		model = Powerplant
		fields = ['name', 'PPE', 'cspr_id', 'is_added']
