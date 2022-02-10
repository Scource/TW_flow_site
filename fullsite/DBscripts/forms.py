from django import forms


class GetPeakValuesForm(forms.Form):
    login = forms.CharField(
        label='Login', required=True)
    password = forms.CharField(
        label='Hasło', required=True, widget=forms.PasswordInput())
    date_from = forms.CharField(
        label='Data', max_length=10, min_length=10, help_text="format (yyyy-mm-dd)", required=True)
    value = forms.IntegerField(label='Wartosc w kWh', required=True)


class GetStandardDataForm(forms.Form):
    login = forms.CharField(
        label='Login', required=True)
    password = forms.CharField(
        label='Hasło', required=True, widget=forms.PasswordInput())
    date_from = forms.CharField(
        label='Data od', max_length=10, min_length=10, help_text="format (yyyy-mm-dd)", required=True)
    date_to = forms.CharField(
        label='Data do', max_length=10, min_length=10, help_text="format (yyyy-mm-dd)", required=True)
    ID = forms.IntegerField(label='ID płachty', required=True)


class GetPPEListForm(forms.Form):
    login = forms.CharField(
        label='Login', required=True)
    password = forms.CharField(
        label='Hasło', required=True, widget=forms.PasswordInput())
    date_from = forms.CharField(
        label='Data od', max_length=10, min_length=10, help_text="format (yyyy-mm-dd)", required=True)
    date_to = forms.CharField(
        label='Data do', max_length=10, min_length=10, help_text="format (yyyy-mm-dd)", required=True)
    ID = forms.IntegerField(label='ID FBT', required=True)
