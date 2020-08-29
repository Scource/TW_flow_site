from django import forms
from .models import tasks, process, comments, posts, files, messages
from bootstrap_datepicker_plus import DateTimePickerInput
from django.forms import modelformset_factory, ClearableFileInput

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
		fields=['proc_process_name', 'proc_description', 'proc_category', 'proc_start_date', 'proc_end_date', 'proc_is_private']
		labels = {
			'proc_process_name': 'Nazwa', 'proc_description': 'Opis', 'proc_category': 'Kategoria', 'proc_start_date': 'Data poczatku', 'proc_end_date': 'Data końca', 'proc_is_private': 'Prywatny proces', 
        }
		widgets = {
            'proc_start_date': DateTimePickerInput(),
            'proc_end_date': DateTimePickerInput(),
            }


class CommForm(forms.ModelForm):
	class Meta:
		model=comments
		fields=['com_body']
		labels = {
            'com_body': '',
        }

class PostsForm(forms.ModelForm):
	class Meta:
		model=posts
		fields=['posts_title', 'posts_text']
		labels = {
            'posts_title': 'Tytuł', 'posts_text': '',
        }



class FileForm(forms.ModelForm):
	class Meta(object):
		model=files
		fields=['files_document']
		widgets = {
            'files_document': ClearableFileInput(attrs={'multiple': True}),
        }

class MessageForm(forms.ModelForm):
	class Meta(object):
		model=messages
		fields=['mess_text']
		labels = {
            'mess_text': '',
        }