from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from .models import tasks, process, comments

from .forms import TaskFormSet, ProcessForm, TaskForm, CommForm, TaskFormPos


from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

from django.http import HttpResponseForbidden

# Create your views here.


def index(request):
	return render(request, 'info_flow/if_index.html')

@login_required
@permission_required('info_flow.view_process')
def if_processes(request):
	proc_list = process.objects.all()
	context={'proc_list':proc_list}
	return render(request, 'info_flow/if_processes.html', context)

@login_required
def if_new_proc(request):
	username=request.user
	if request.method=='POST':
		process_form=ProcessForm(request.POST)
		if process_form.is_valid(): 
			newProcess=process_form.save(commit=False)
			newProcess.proc_author_id=request.user.id
			newProcess.save()

			if 'save_process' in request.POST:
				return redirect('info_flow:if_processes')
			elif 'add_tasks' in request.POST:
				return redirect('info_flow:if_add_task', pid=newProcess.id)
	else:

		process_form=ProcessForm()
		context={'process_form':process_form}
	return render(request, 'info_flow/if_new_proc.html', context)

@login_required
def if_add_task(request, pid):
	proc=process.objects.get(pk = pid)
	if not request.user.id==proc.proc_author.id:
		return HttpResponseForbidden("You are not allowed to edit thissfasfasf Post")
	if request.method=='POST':
		task_form=TaskFormSet(request.POST)
		if task_form.is_valid():
			for form in task_form:
				newTask=form.save(commit=False)
				newTask.tasks_proc_id=pid
				newTask.save()
		return redirect('info_flow:if_processes')
	else:
		task_form=TaskFormSet(queryset=tasks.objects.none())
		context={'task_form':task_form, 'proc':proc}
	return render(request, 'info_flow/if_add_task.html', context)

@login_required
@permission_required('info_flow.view_process')
def if_show_proc(request, pid):
	if request.method=='POST':
		com_form=CommForm(request.POST)
		if com_form.is_valid():
			newCom=com_form.save(commit=False)
			newCom.com_author_id=1
			newCom.com_proc_id=pid
			com_form.save()
		return redirect('info_flow:if_show_proc', pid=pid)

	else:
		com_form=CommForm()
		coms=comments.objects.all().filter(com_proc_id=pid)
		proc=process.objects.get(pk = pid)
		task=tasks.objects.all().filter(tasks_proc_id=pid)
		context={'proc':proc,'task':task, 'com_form':com_form, 'coms':coms}
	return render(request, 'info_flow/if_show_proc.html', context)

@login_required
#@permission_required('polls.can_vote', raise_exception=True)
def if_edit_proc(request, pid):
	proc=process.objects.get(pk = pid)
	if not request.user.id==proc.proc_author.id:
		return HttpResponseForbidden("You are not allowed to edit thissfasfasf Post")
	task=tasks.objects.all().filter(tasks_proc_id=pid)
	if request.method=='POST':
		proc_form=ProcessForm(request.POST, instance=proc)		
		task_form=TaskFormPos(request.POST)
		if proc_form.is_valid():
			proc_form.save()
		if task_form.is_valid():
			for form in task_form:
				if form.is_valid():
					newForm=form.save(commit=False)
					newForm.tasks_proc_id=pid
					newForm.save()
		return redirect('info_flow:if_show_proc', pid=pid)

	else:		
		proc_form=ProcessForm(instance=proc)		
		task_form=TaskFormPos(queryset=tasks.objects.none())
		context={'proc':proc,'task':task, 'proc_form':proc_form, 'task_form':task_form}
	return render(request, 'info_flow/if_edit_proc.html', context)

