from django import forms


class ScriptsForm(forms.Form):
    login = forms.CharField(
        label='Login', required=True)
    password = forms.CharField(
        label='Hasło', required=True)
    date_from = forms.CharField(
        label='Data', max_length=10, min_length=10, help_text="format (yyyy-mm-dd)", required=True)
    ID = forms.IntegerField(label='Wartosc w kWh', required=True)


