from django import forms
from .models import tasks, process, comments
from bootstrap_datepicker_plus import DateTimePickerInput
from django.forms import modelformset_factory

class TaskForm(forms.ModelForm):

	class Meta:
		model = tasks
		fields =['tasks_name', 'tasks_description', 'tasks_start_date', 'tasks_end_date', 'tasks_assigned', 'tasks_is_active']
		widgets = {
            'tasks_start_date': DateTimePickerInput(),
            'tasks_end_date': DateTimePickerInput(),
            #'tasks_proc': forms.HiddenInput()

            }


TaskFormSet=modelformset_factory(tasks, form=TaskForm, extra=1)
TaskFormPos=modelformset_factory(tasks, form=TaskForm, extra=0)

 #extra=1, fields =('tasks_name', 'tasks_description', 'tasks_deadline_dt', 'tasks_assigned', 'tasks_is_active'))



class ProcessForm(forms.ModelForm):
	class Meta:
		model=process
		fields=['proc_process_name', 'proc_description', 'proc_category', 'proc_start_date', 'proc_end_date', 'proc_is_active', 'proc_is_private']
		widgets = {
            'proc_start_date': DateTimePickerInput(),
            'proc_end_date': DateTimePickerInput(),
            }


class CommForm(forms.ModelForm):
	class Meta:
		model=comments
		fields=['com_body']
