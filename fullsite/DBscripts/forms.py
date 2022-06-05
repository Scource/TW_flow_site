from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from BalancingMarket.models import Element


class DateInput(forms.DateInput):
    input_type = 'date'
    format='%Y-%m-%d'

class GetPeakValuesForm(forms.Form):
    date_from = forms.DateField(widget=DateInput(), label='Data')
    value = forms.IntegerField(label='Wartosc w kWh', required=True)



class GetStandardDataForm(forms.Form):
    date_from = forms.DateField(widget=DateInput(), label='Data od')
    date_to = forms.DateField(widget=DateInput(), label='Data do')
    #ID = forms.IntegerField(label='ID płachty', required=True)
    POB_elements = forms.ModelMultipleChoiceField(queryset=Element.objects.filter(element_type=0
                ).order_by('code'), widget=FilteredSelectMultiple("", is_stacked=False), label='POB')

    class Media:
        js = ( 'admin/js/jquery.init.js', 'admin/js/vendor/jquery/jquery.js','/jsi18n/' )
        #js = ( '/jquery.js','/jsi18n/')

    def clean(self):
        # data from the form is fetched using super function
        super(GetStandardDataForm, self).clean()

        dt_from = self.cleaned_data.get('date_from')
        dt_to = self.cleaned_data.get('date_to')
        if dt_from > dt_to:
            self._errors['text'] = self.error_class([
                'Błędna data'])

        # return any errors if found
        return self.cleaned_data

class GetWIREDataForm(GetStandardDataForm, forms.Form):
    rdg = forms.BooleanField(label='Generacja RDG', required=False)
    get_all_FBT = forms.BooleanField(label='Wymagające korekt', required=False)

