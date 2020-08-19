from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, FileResponse
from .models import tasks, process, comments, posts, messages, files

from .forms import TaskFormSet, ProcessForm, TaskForm, CommForm, TaskFormPos, PostsForm, FileForm, MessageForm

from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

from django.http import HttpResponseForbidden
import mimetypes


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
		file_form=FileForm(request.POST, request.FILES)
		if process_form.is_valid() & file_form.is_valid():
			newProcess=process_form.save(commit=False)
			newProcess.proc_author_id=request.user.id
			newProcess.save()

			newFile=file_form.save(commit=False)
			newFile.files_proc_id=newProcess.id
			newFile.files_by_user_id=request.user.id
			newFile.files_name=request.FILES['files_document'].name
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
			newCom.com_author_id=request.user.id
			newCom.com_proc_id=pid
			com_form.save()
		return redirect('info_flow:if_show_proc', pid=pid)

	else:
		com_form=CommForm()
		fi=files.objects.all().filter(files_proc_id = pid)
		coms=comments.objects.all().filter(com_proc_id=pid)
		proc=process.objects.get(pk = pid)
		task=tasks.objects.all().filter(tasks_proc_id=pid)
		context={'proc':proc,'task':task, 'com_form':com_form, 'coms':coms, 'fi':fi}
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


@login_required
def if_post_list(request):
	post_list=posts.objects.all()
	context={'post_list':post_list}
	return render(request, 'info_flow/if_post_list.html' ,context)



@login_required
def if_new_post(request):
	if request.method=='POST':
		post_form=PostsForm(request.POST)		
		if post_form.is_valid():
			newPost=post_form.save(commit=False)
			newPost.posts_author=request.user
			newPost.save()
		return redirect('info_flow:if_post_list')
	else:
		post_form=PostsForm()
		context={'post_form':post_form}
		return render(request, 'info_flow/if_new_post.html', context)


@login_required
def if_show_post(request, pid):
	post=posts.objects.get(pk = pid)
	mess=messages.objects.all().filter(mess_posts_id=pid)
	mess_form=MessageForm()
	context={'post':post, 'mess':mess, 'mess_form':mess_form}

	return render(request, 'info_flow/if_show_post.html', context)

@ensure_csrf_cookie
@csrf_protect
@login_required
def if_add_message(request):
	if request.is_ajax and request.method == "POST":
		messForm=MessageForm(request.POST)
		post_id=request.POST['post_id']
		if messForm.is_valid():

			newMes=messForm.save(commit=False)
			newMes.mess_author = request.user
			newMes.mess_posts_id = post_id
		
			newMes.save()
			return HttpResponse('success')
	else:
		return HttpResponse("unsuccesful")

@login_required
def if_edit_post(request, pid):
	post=posts.objects.get(pk = pid)
	if not request.user.id==post.posts_author.id:
		return HttpResponseForbidden("You are not allowed to edit thissfasfasf Post")
	if request.method=='POST':
		post_form=PostsForm(request.POST, instance=post)		
		if post_form.is_valid():
			post_form.save()
		return redirect('info_flow:if_show_post', pid=pid)

	else:		
		post_form=PostsForm(instance=post)		
		context={'post_form':post_form, 'post':post}
	return render(request, 'info_flow/if_edit_post.html', context)


@login_required
def download_file(request, fid):
    # fill these variables with real values
    obj = files.objects.get(pk=fid)
    filename = obj.files_document.url
    name = obj.files_name
    response = FileResponse(open(filename, 'rb'))
    response['Content-Disposition'] = "attachment; filename=" + name
    return response

    # fl_path = files.objects.get(id=fid).files_document
    # filename = files.objects.get(id=fid).files_name

    # fl = open(fl_path, 'rb')
    # mime_type, _ = mimetypes.guess_type(fl_path)
    # response = HttpResponse(fl, content_type=mime_type)
    # response['Content-Disposition'] = "attachment; filename=%s" % filename
    # return response
