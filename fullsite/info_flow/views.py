from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, FileResponse
from .models import tasks, process, comments, posts, messages, files

from .forms import TaskFormSet, ProcessForm, TaskForm, CommForm, TaskFormPos, PostsForm, FileForm, MessageForm

from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

from django.http import HttpResponseForbidden
import mimetypes
import os
from django.conf import settings


# Create your views here.


def index(request):
	return render(request, 'info_flow/if_index.html')

@login_required
@permission_required('info_flow.view_process')
def if_processes(request):
	proc_list = process.objects.all().filter(proc_is_deleted=False)
	context={'proc_list':proc_list}
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
				return redirect('info_flow:if_processes')
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
		task=tasks.objects.all().filter(tasks_proc_id=pid, tasks_is_deleted=False)
		context={'proc':proc,'task':task, 'com_form':com_form, 'coms':coms, 'fi':fi}
	return render(request, 'info_flow/if_show_proc.html', context)

@login_required
@permission_required('info_flow.change_process')
def if_edit_proc(request, pid):
	proc=process.objects.get(pk = pid)
	if not request.user.id==proc.proc_author.id:
		return HttpResponseForbidden("Nie ma takiego podgladania")
	task=tasks.objects.all().filter(tasks_proc_id=pid, tasks_is_deleted=False)
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
@permission_required('info_flow.delete_process')
def if_delete_proc(request, proc_id):
    delete_proc=process.objects.get(id=proc_id)
    delete_proc.proc_is_deleted = True
    delete_proc.save()
    del_conn_com=comments.objects.all().filter(com_proc_id=proc_id).update(com_is_deleted=True)
    deleted_files=files.objects.all().filter(files_proc_id=proc_id).update(files_is_deleted=True)
    return redirect('info_flow:if_processes')



@login_required
@permission_required('info_flow.view_posts')
def if_post_list(request):
	post_list=posts.objects.all().filter(posts_is_deleted=False)
	context={'post_list':post_list}
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

	context={'post':post, 'mess':mess, 'mess_form':mess_form}
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