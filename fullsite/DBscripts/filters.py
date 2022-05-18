import django_filters
from .models import Report


class ReportFilter(django_filters.FilterSet):
	CHOICES = ((None, '-----------'), (False, 'Nieuzupełniona'),
	           (True, 'Uzupełniona'))

	report_type = django_filters.CharFilter(
		field_name='report_type', lookup_expr='icontains')
	start = django_filters.DateFilter(
        'start',
            lookup_expr='date')
	end = django_filters.DateFilter(
            'end',
            lookup_expr='date')
	
	class Meta:
		model = Report
		fields = ['start', 'end', 'report_type']

