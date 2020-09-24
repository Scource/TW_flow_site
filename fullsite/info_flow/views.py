from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, FileResponse
from .models import tasks, process, comments, posts, messages, files, category
from .filters import ProcessFilter, PostsFilter
from .forms import TaskFormSet, ProcessForm, TaskForm, CommForm, TaskFormPos, PostsForm, FileForm, MessageForm, TaskFormPoint, TaskFormPointEdit

from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

from django.http import HttpResponseForbidden
import mimetypes
import os
from django.conf import settings
from .services import get_tasks_in_proc, get_points_in_task


# Create your views here.


def index(request):
	return render(request, 'info_flow/if_index.html')

#@userpasstest decorator check!
@login_required
@permission_required('info_flow.view_process')
def if_processes(request, cat):
	# if not request.user.groups.filter(name=cat).exists():
	# 	return HttpResponseForbidden("Nie ma takiego podgladania")
	cat_id=category.objects.get(cat_name=cat).id
	proc_list = process.objects.all().filter(proc_is_deleted=False, proc_is_private=False, proc_category=cat_id)
	proc_f=ProcessFilter(request.GET, queryset=proc_list)
	context={'proc_list':proc_list, 'proc_f':proc_f, }
	return render(request, 'info_flow/if_processes.html', context)


@login_required
@permission_required('info_flow.add_process')
def if_new_proc(request):
	username=request.user
	if request.method=='POST':
		process_form=ProcessForm(request.POST)
		file_form=FileForm(request.POST, request.FILES)
		if process_form.is_valid() & file_form.is_valid():
			newProcess=process_form.save(commit=False)
			newProcess.proc_author_id=request.user.id
			newProcess.save()
			for f in request.FILES.getlist('files_document'):
				#newFile=f.save(commit=False)
				newFile = files(files_document=f)
				newFile.files_proc_id=newProcess.id
				newFile.files_by_user_id=request.user.id
				newFile.files_name=f
				newFile.save()

			if 'save_process' in request.POST:
				return redirect('info_flow:if_processes', cat=newProcess.proc_category)
			elif 'add_tasks' in request.POST:
				return redirect('info_flow:if_add_task', pid=newProcess.id)
	else:
		file_form=FileForm()
		process_form=ProcessForm()
		context={'process_form':process_form, 'file_form':file_form}
		return render(request, 'info_flow/if_new_proc.html', context)


@login_required
@permission_required('info_flow.add_tasks')
def if_add_task(request, pid):
	proc=process.objects.get(pk = pid)
	if not request.user.id==proc.proc_author.id:
		return HttpResponseForbidden("Nie ma takiego podgladania")
	if request.method=='POST':

		task_form=TaskForm(request.POST)
		file_form=FileForm(request.POST, request.FILES)
		if task_form.is_valid() & file_form.is_valid():
			newTask=task_form.save(commit=False)
			newTask.tasks_proc_id=pid
			newTask.save()
			for f in request.FILES.getlist('files_document'):
				#newFile=f.save(commit=False)
				newFile = files(files_document=f)
				newFile.files_tasks_id=newTask.id
				newFile.files_by_user_id=request.user.id
				newFile.files_name=f
				newFile.save()
			if 'save_process' in request.POST:
				return redirect('info_flow:if_processes', cat=proc.proc_category)
			elif 'save_task' in request.POST:
				return redirect('info_flow:if_add_task', pid=pid)
			elif 'add_point' in request.POST:
				return redirect('info_flow:if_add_point', tid=newTask.id)
	else:
		file_form=FileForm()
		task_form=TaskForm()
		context={'task_form':task_form, 'file_form':file_form, 'proc':proc}
		return render(request, 'info_flow/if_add_task.html', context)


@login_required
@permission_required('info_flow.delete_tasks')
def if_delete_task(request, task_id):
    delete_tasks=tasks.objects.get(id=task_id)
    proc_id=delete_tasks.tasks_proc_id
    delete_tasks.tasks_is_deleted = True
    delete_tasks.save()
    return redirect('info_flow:if_edit_proc', pid=proc_id)


@login_required
@permission_required('info_flow.view_process')
def if_show_proc(request, pid):
	tasks_data = get_tasks_in_proc(pid)
	if request.method=='POST':
		com_form=CommForm(request.POST)
		if com_form.is_valid():
			newCom=com_form.save(commit=False)
			newCom.com_author_id=request.user.id
			newCom.com_proc_id=pid
			com_form.save()
		return redirect('info_flow:if_show_proc', pid=pid)

	else:
		com_form=CommForm()
		fi=files.objects.all().filter(files_proc_id = pid)
		coms=comments.objects.all().filter(com_proc_id=pid)
		proc=process.objects.get(pk = pid)
		task=tasks.objects.all().filter(tasks_proc_id=pid, tasks_is_deleted=False, tasks_tasks_id__isnull=True)
		context={'proc':proc,'task':task, 'com_form':com_form, 'coms':coms, 'fi':fi, 'tasks_data':tasks_data}
	return render(request, 'info_flow/if_show_proc.html', context)


@login_required
@permission_required('info_flow.view_tasks')
def if_show_task(request, tid):
	points_data=get_points_in_task(tid)
	fi=files.objects.all().filter(files_tasks_id = tid)
	task=tasks.objects.get(pk = tid)
	point=tasks.objects.all().filter(tasks_tasks_id=tid, tasks_is_deleted=False)
	context={'point':point,'task':task, 'fi':fi, 'points_data':points_data}
	return render(request, 'info_flow/if_show_task.html', context)

@login_required
@permission_required('info_flow.change_process')
def if_edit_proc(request, pid):
	proc=process.objects.get(pk = pid)
	if not request.user.id==proc.proc_author.id:
		return HttpResponseForbidden("Nie ma takiego podgladania")
	task=tasks.objects.all().filter(tasks_proc_id=pid, tasks_is_deleted=False, tasks_tasks_id__isnull=True)
	if request.method=='POST':
		file_form=FileForm(request.POST, request.FILES)
		proc_form=ProcessForm(request.POST, instance=proc)		
		task_form=TaskFormPos(request.POST)
		if proc_form.is_valid()  & file_form.is_valid():
			proc_form.save()
			for f in request.FILES.getlist('files_document'):
				newFile = files(files_document=f)
				newFile.files_proc_id=pid
				newFile.files_by_user_id=request.user.id
				newFile.files_name=f
				newFile.save()
		if task_form.is_valid():
			for form in task_form:
				if form.is_valid():
					newForm=form.save(commit=False)
					newForm.tasks_proc_id=pid
					newForm.save()
		return redirect('info_flow:if_show_proc', pid=pid)
	else:
		file_form=FileForm()
		fi=files.objects.all().filter(files_proc_id = pid)
		proc_form=ProcessForm(instance=proc)		
		task_form=TaskFormPos(queryset=tasks.objects.none())
		context={'proc':proc,'task':task, 'proc_form':proc_form, 'task_form':task_form, 'fi':fi, 'file_form':file_form}
	return render(request, 'info_flow/if_edit_proc.html', context)


@login_required
@permission_required('info_flow.change_tasks')
def if_edit_task(request, tid):
	task=tasks.objects.get(pk = tid)
	# if not request.user.id==proc.proc_author.id:
	# 	return HttpResponseForbidden("Nie ma takiego podgladania")
	point=tasks.objects.all().filter(tasks_tasks_id=tid, tasks_is_deleted=False)
	if request.method=='POST':
		file_form=FileForm(request.POST, request.FILES)
		task_form=TaskForm(request.POST, instance=task)
		point_form=TaskFormPointEdit(request.POST)
		if task_form.is_valid()  & file_form.is_valid():
			task_form.save()
			for f in request.FILES.getlist('files_document'):
				newFile = files(files_document=f)
				newFile.files_tasks_id=tid
				newFile.files_by_user_id=request.user.id
				newFile.files_name=f
				newFile.save()
		if point_form.is_valid():
			for form in point_form:
				if form.is_valid():
					newForm=form.save(commit=False)
					newForm.tasks_proc_id=task.tasks_proc_id
					newForm.tasks_tasks_id=tid
					newForm.save()
		return redirect('info_flow:if_show_task', tid=tid)
	else:
		file_form=FileForm()
		fi=files.objects.all().filter(files_tasks_id = tid)
		task_form=TaskForm(instance=task)		
		point_form=TaskFormPointEdit(queryset=tasks.objects.none())
		context={'point':point, 'task':task, 'point_form':point_form, 'task_form':task_form, 'fi':fi, 'file_form':file_form}
	return render(request, 'info_flow/if_edit_task.html', context)


@login_required
@permission_required('info_flow.delete_process')
def if_delete_proc(request, proc_id):
    delete_proc=process.objects.get(id=proc_id)
    delete_proc.proc_is_deleted = True
    delete_proc.save()
    del_conn_com=comments.objects.all().filter(com_proc_id=proc_id).update(com_is_deleted=True)
    del_conn_task=tasks.objects.all().filter(tasks_proc_id=proc_id).update(tasks_is_deleted=True)
    deleted_files=files.objects.all().filter(files_proc_id=proc_id).update(files_is_deleted=True)
    return redirect('info_flow:if_processes', cat=delete_proc.proc_category)


@login_required

def if_add_point(request, tid):
	task=tasks.objects.get(pk = tid)
	if request.method=='POST':
		point_form=TaskFormPoint(request.POST)
		if point_form.is_valid():
			for form in point_form:
				newPoint=form.save(commit=False)
				newPoint.tasks_proc_id=task.tasks_proc_id
				newPoint.tasks_tasks_id=tid
				newPoint.save()
			if 'save_process' in request.POST:
				return redirect('info_flow:if_processes', cat=process.objects.get(id=task.tasks_proc_id).proc_category)
			elif 'add_task' in request.POST:
				return redirect('info_flow:if_add_task', pid=task.tasks_proc_id)
	else:
		point_form=TaskFormPoint(queryset=tasks.objects.none())
		context={'point_form':point_form, 'task':task}
		return render(request, 'info_flow/if_add_point.html', context)


@login_required
@permission_required('info_flow.view_posts')
def if_post_list(request):
	post_list=posts.objects.all().filter(posts_is_deleted=False)
	posts_f=PostsFilter(request.GET, queryset=post_list)
	context={'posts_f':posts_f}
	return render(request, 'info_flow/if_post_list.html' ,context)



@login_required
@permission_required('info_flow.add_posts')
def if_new_post(request):
	if request.method=='POST':
		post_form=PostsForm(request.POST)
		file_form=FileForm(request.POST, request.FILES)		
		if post_form.is_valid() & file_form.is_valid():
			newPost=post_form.save(commit=False)
			newPost.posts_author=request.user
			newPost.save()
			for f in request.FILES.getlist('files_document'):
				newFile = files(files_document=f)
				newFile.files_posts_id=newPost.id
				newFile.files_by_user_id=request.user.id
				newFile.files_name=f
				newFile.save()

		return redirect('info_flow:if_post_list')
	else:
		file_form=FileForm()
		post_form=PostsForm()
		context={'post_form':post_form, 'file_form':file_form}
		return render(request, 'info_flow/if_new_post.html', context)


@login_required
@permission_required('info_flow.view_posts')
def if_show_post(request, pid):
	post=posts.objects.get(pk = pid)
	fi=files.objects.all().filter(files_posts_id = pid)
	mess=messages.objects.all().filter(mess_posts_id=pid, mess_is_deleted=False)
	mess_form=MessageForm()
	if request.method=='POST':
		messForm=MessageForm(request.POST)		
		if messForm.is_valid():
			newMes=messForm.save(commit=False)
			newMes.mess_author = request.user
			newMes.mess_posts_id = pid
			newMes.save()
		return redirect('info_flow:if_show_post', pid=pid)

	context={'post':post, 'mess':mess, 'mess_form':mess_form, 'fi':fi}
	return render(request, 'info_flow/if_show_post.html', context)


@login_required
@permission_required('info_flow.delete_messages')
def if_del_mess(request, mess_id):
    delete_mess=messages.objects.get(id=mess_id)
    postid=delete_mess.mess_posts_id
    delete_mess.mess_is_deleted = True
    delete_mess.save()
    return redirect('info_flow:if_show_post', pid=postid)

@login_required
@permission_required('info_flow.delete_posts')
def if_delete_post(request, post_id):
    delete_post=posts.objects.get(id=post_id)
    delete_post.posts_is_deleted = True
    delete_post.save()
    del_conn_mess=messages.objects.all().filter(mess_posts_id=post_id).update(mess_is_deleted=True)
    deleted_files=files.objects.all().filter(files_posts_id=post_id).update(files_is_deleted=True)
    return redirect('info_flow:if_post_list')


@login_required
@permission_required('info_flow.change_posts')
def if_edit_post(request, pid):
	post=posts.objects.get(pk = pid)
	if not request.user.id==post.posts_author.id:
		return HttpResponseForbidden("Nie ma takiego podgaldania")
	if request.method=='POST':
		post_form=PostsForm(request.POST, instance=post)
		file_form=FileForm(request.POST, request.FILES)	
		if post_form.is_valid() & file_form.is_valid():
			post_form.save()
			for f in request.FILES.getlist('files_document'):
				newFile = files(files_document=f)
				newFile.files_posts_id=pid
				newFile.files_by_user_id=request.user.id
				newFile.files_name=f
				newFile.save()
		return redirect('info_flow:if_show_post', pid=pid)

	else:
		fi=files.objects.all().filter(files_posts_id = pid)
		file_form=FileForm()
		post_form=PostsForm(instance=post)		
		context={'post_form':post_form, 'post':post, 'file_form':file_form, 'fi':fi }
	return render(request, 'info_flow/if_edit_post.html', context)


@login_required
@permission_required('info_flow.view_files')
def download_file(request, fid):
    # fill these variables with real values
    obj = files.objects.get(pk=fid)
    filename = settings.BASE_DIR+obj.files_document.url
    name = obj.files_name
    response = FileResponse(open(filename, 'rb'))
    response['Content-Disposition'] = "attachment; filename=" + name
    return response



### ZAMIENIĆ TE 3 jakoś na 1############
@login_required
@permission_required('info_flow.delete_files')
def if_delete_file(request, file_id):
    delete_file=files.objects.get(id=file_id)
    proc_id=delete_file.files_proc_id
    delete_file.delete()
    delete_file.delete_file()
    return redirect('info_flow:if_edit_proc', pid=proc_id)

@login_required
@permission_required('info_flow.delete_files')
def if_delete_post_file(request, file_id):
    delete_file=files.objects.get(id=file_id)
    post_id=delete_file.files_posts_id
    delete_file.delete()
    delete_file.delete_file()
    return redirect('info_flow:if_edit_post', pid=post_id)


@login_required
@permission_required('info_flow.delete_files')
def if_delete_post_file(request, file_id):
    delete_file=files.objects.get(id=file_id)
    task_id=delete_file.files_tasks_id
    delete_file.delete()
    delete_file.delete_file()
    return redirect('info_flow:if_edit_task', pid=task_id)


@login_required
def user_profile(request):
	priv_proc=process.objects.all().filter(proc_is_private=True, proc_author=request.user, proc_is_deleted=False)
	user_proc=process.objects.all().filter(proc_assigned_id=request.user, proc_is_deleted=False, proc_is_private=False)
	user_tasks=tasks.objects.all().filter(tasks_assigned_id=request.user, tasks_is_deleted=False)
	context={'user_proc':user_proc, 'user_tasks':user_tasks, 'priv_proc':priv_proc}
	return render(request, 'info_flow/user_profile.html', context)

@login_required
def accept_task(request, task_id):
	tasks.toggle_active(task_id)
	return redirect('info_flow:if_show_task', tid=task_id)


@login_required
def assign_task(request, task_id):
	user=request.user
	redirect_id=tasks.set_assignation(task_id, user)
	return redirect('info_flow:if_show_task', tid=redirect_id)
