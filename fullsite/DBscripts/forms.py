from django import forms


class ScriptsForm(forms.Form):
    date_from = forms.CharField(
        label='Data od', max_length=10, min_length=10, help_text="format (yyyy-mm-dd)", required=True)
    date_to = forms.CharField(
        label='Data do', max_length=10, min_length=10, help_text="format (yyyy-mm-dd)", required=True)
    ID = forms.IntegerField(label='ID Płachty', required=True)


