from django import forms
from .models import *
from django.contrib.admin import widgets


class DateInput(forms.DateInput):
	input_type = 'date'


class ElementForm(forms.ModelForm):
	class Meta:
		model = Element
		fields = ['code', 'name', 'dt_from', 'dt_to', 'cspr_id', 'old_skome_id', 'wire_id', 'rher_id', 'element_type', 'is_added']
		widgets = {
                    'dt_from': DateInput(),
                    'dt_to': DateInput()
                }


class ElementFileForm(forms.ModelForm):
	class Meta:
		model = File
		fields = ['document']
		widgets = {
                    'document': forms.ClearableFileInput(attrs={'multiple': True})
                }


class ConnectionForm(forms.ModelForm):
	class Meta:
		model = Connection
		fields = ['POB', 'SE', 'dt_from', 'dt_to']
		widgets = {
                    'dt_from': DateInput(),
                    'dt_to': DateInput()
        }

class PowerplantForm(forms.ModelForm):
	class Meta:
		model = Powerplant
		fields = ['name', 'PPE', 'cspr_id', 'element_type', 'is_added']



class PowerplantConnectionForm(forms.ModelForm):
	class Meta:
		model = PowerPlantConnection
		fields = ['POB', 'powerplant', 'dt_from', 'dt_to']
		widgets = {
                    'POB': forms.Select(),
                    'dt_from': DateInput(),
                    'dt_to': DateInput()
		}
