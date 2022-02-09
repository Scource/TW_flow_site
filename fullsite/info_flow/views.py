from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, FileResponse
from django.core.exceptions import PermissionDenied
from django.db.models import Max, Q
from .models import tasks, process, comments, posts, messages, files, category, patterns_elements, patterns
from .filters import ProcessFilter, PostsFilter, UserProcessFilter, UsersFilter, UserTasksFilter, PatternFilter
from .forms import TaskFormSet, ProcessForm, TaskForm, CommForm, TaskFormPos, PostsForm, FileForm, MessageForm, TaskFormPoint, TaskFormPointEdit, PatternForm, CreateFromPattern, Edit_pattern_elements
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

from django.http import HttpResponseForbidden, HttpResponseRedirect
import mimetypes
import os
from django.conf import settings
from .services import get_tasks_in_proc, get_points_in_task, get_proc_elemenets, create_proc_from_pattern, save_pattern
from .permissions import add_perms_to_new_object, toggle_perm_on_object, set_perm_to_subs
from django.contrib.auth import get_user_model
from guardian.shortcuts import assign_perm, get_objects_for_user, get_users_with_perms, get_perms
# Create your views here.
User = get_user_model()


def index(request):
    newest_proc = get_objects_for_user(request.user, 'info_flow.connect_proc', process.objects.filter(
        proc_is_deleted=False, proc_is_private=False).order_by('-proc_created'))
    newest_proc_list = newest_proc[:4]
    newest_posts = posts.objects.filter(
        posts_is_deleted=False).order_by('-posts_created')
    newest_post_list = newest_posts[:4]
    context = {'newest_proc_list': newest_proc_list,
               'newest_post_list': newest_post_list}
    return render(request, 'info_flow/if_index.html', context)


@login_required
@permission_required('info_flow.view_process')
def if_processes(request, cat, active):
    if active == "active":
        state = True
    else:
        state = False
    cat_id = category.objects.get(cat_name=cat).id
    proc_list = get_objects_for_user(request.user, 'info_flow.connect_proc', process.objects.filter(
        proc_is_deleted=False, proc_is_private=False, proc_category=cat_id, proc_is_active=state), accept_global_perms=False)
    proc_f = ProcessFilter(request.GET, queryset=proc_list)
    context = {'proc_f': proc_f, 'cat': cat, 'state': state}
    return render(request, 'info_flow/if_processes.html', context)


@login_required
@permission_required('info_flow.view_process')
def if_process_list(request):
    return render(request, 'info_flow/if_process_list.html')


@login_required
@permission_required('info_flow.add_process')
def if_new_proc(request):
    username = request.user
    if request.method == 'POST':
        process_form = ProcessForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)
        if process_form.is_valid() & file_form.is_valid():
            print('aaa')
            newProcess = process_form.save(commit=False)
            newProcess.proc_is_active = True
            newProcess.proc_author_id = request.user.id
            newProcess.save()
            add_perms_to_new_object(request.user, newProcess, 'proc')
            for f in request.FILES.getlist('files_document'):
                # newFile=f.save(commit=False)
                newFile = files(files_document=f)
                newFile.files_proc_id = newProcess.id
                newFile.files_by_user_id = request.user.id
                newFile.files_name = f
                newFile.save()
            if 'save_process' in request.POST:
                return redirect('info_flow:if_processes', cat=newProcess.proc_category, active='active')
            elif 'add_tasks' in request.POST:
                return redirect('info_flow:if_add_task', pid=newProcess.id)
    else:
        file_form = FileForm()
        process_form = ProcessForm()
        context = {'process_form': process_form, 'file_form': file_form}
        return render(request, 'info_flow/if_new_proc.html', context)


@login_required
@permission_required('info_flow.add_tasks')
def if_add_task(request, pid):
    proc = process.objects.get(pk=pid)
    if not (request.user.id == proc.proc_author.id or request.user.id == proc.proc_assigned.id):
        raise PermissionDenied
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)
        if task_form.is_valid() & file_form.is_valid():
            newTask = task_form.save(commit=False)
            newTask.tasks_is_active = True
            newTask.tasks_proc_id = pid
            newTask.tasks_author_id = request.user.id
            newTask.save()
            task_form.save_m2m()
            add_perms_to_new_object(request.user, newTask, 'task')
            for f in request.FILES.getlist('files_document'):
                newFile = files(files_document=f)
                newFile.files_tasks_id = newTask.id
                newFile.files_by_user_id = request.user.id
                newFile.files_name = f
                newFile.save()
            if 'save_process' in request.POST:
                return redirect('info_flow:if_processes', cat=proc.proc_category, active='active')
            elif 'save_task' in request.POST:
                return redirect('info_flow:if_add_task', pid=pid)
            elif 'add_point' in request.POST:
                return redirect('info_flow:if_add_point', tid=newTask.id)

    else:
        file_form = FileForm()
        task_form = TaskForm()
        context = {'task_form': task_form,
                   'file_form': file_form, 'proc': proc}
        return render(request, 'info_flow/if_add_task.html', context)


@login_required
@permission_required('info_flow.delete_tasks')
def if_delete_task(request, task_id):
    delete_tasks = tasks.objects.get(id=task_id)
    if not (request.user.id == delete_tasks.tasks_proc.proc_author.id or request.user.id == delete_tasks.tasks_author.id):
        try:
            if not request.user in delete_tasks.tasks_assigned.all():
                raise PermissionDenied
        except AttributeError:
            raise PermissionDenied
    proc_id = delete_tasks.tasks_proc_id
    delete_tasks.tasks_is_deleted = True
    delete_tasks.save()
    if delete_tasks.tasks_tasks_id == None:
        return redirect('info_flow:if_edit_proc', pid=proc_id)
    else:
        return redirect('info_flow:if_edit_task', tid=delete_tasks.tasks_tasks_id)


@login_required
@permission_required('info_flow.view_process')
def if_show_proc(request, pid):
    proc = process.objects.get(pk=pid)
    if not 'connect_proc' in get_perms(request.user, proc):
        raise PermissionDenied
    tasks_data = get_tasks_in_proc(pid)
    if request.method == 'POST':
        com_form = CommForm(request.POST)
        if com_form.is_valid():
            newCom = com_form.save(commit=False)
            newCom.com_author_id = request.user.id
            newCom.com_proc_id = pid
            newCom.save()
        return redirect('info_flow:if_show_proc', pid=pid)

    else:
        com_form = CommForm()
        fi = files.objects.filter(files_proc_id=pid)
        coms = comments.objects.filter(com_proc_id=pid, com_is_deleted=False)
        task_list = get_objects_for_user(request.user, 'info_flow.connect_task', tasks.objects.filter(
            tasks_proc_id=pid, tasks_is_deleted=False, tasks_tasks_id__isnull=True), accept_global_perms=False)
        task = task_list.order_by('tasks_created')
        context = {'proc': proc, 'task': task, 'com_form': com_form,
                   'coms': coms, 'fi': fi, 'tasks_data': tasks_data}
    return render(request, 'info_flow/if_show_proc.html', context)


@login_required
@permission_required('info_flow.view_tasks')
def if_show_task(request, tid):
    task = tasks.objects.get(pk=tid)
    if not 'connect_task' in get_perms(request.user, task):
        raise PermissionDenied
    if request.method == 'POST':
        file_form = FileForm(request.POST, request.FILES)
        com_form = CommForm(request.POST)
        if file_form.is_valid():
            for f in request.FILES.getlist('files_document'):
                newFile = files(files_document=f)
                newFile.files_tasks_id = tid
                newFile.files_by_user_id = request.user.id
                newFile.files_name = f
                newFile.save()
        else:
            return redirect('info_flow:if_show_task', tid=tid)
        if com_form.is_valid():
            newCom = com_form.save(commit=False)
            newCom.com_author_id = request.user.id
            newCom.com_tasks_id = tid
            newCom.save()
            if task.tasks_tasks_id == None:
                return redirect('info_flow:if_show_task', tid=tid)
            else:
                return redirect('info_flow:if_show_point', tid=tid)
        else:
            if task.tasks_tasks_id == None:
                return redirect('info_flow:if_show_task', tid=tid)
            else:
                return redirect('info_flow:if_show_point', tid=tid)
    else:
        file_form = FileForm()
        com_form = CommForm()
        points_data = get_points_in_task(tid)
        coms = comments.objects.filter(com_tasks_id=tid, com_is_deleted=False)
        fi = files.objects.all().filter(files_tasks_id=tid)
        #point=tasks.objects.filter(tasks_tasks_id=tid, tasks_is_deleted=False)
        point_list = get_objects_for_user(request.user, 'info_flow.connect_task', tasks.objects.filter(
            tasks_tasks_id=tid, tasks_is_deleted=False), accept_global_perms=False)
        point = point_list.order_by('tasks_created')
        context = {'point': point, 'task': task, 'fi': fi, 'points_data': points_data,
                   'com_form': com_form, 'coms': coms, 'file_form': file_form}
        if task.tasks_tasks_id == None:
            return render(request, 'info_flow/if_show_task.html', context)
        else:
            return render(request, 'info_flow/if_show_point.html', context)


@login_required
@permission_required('info_flow.change_process')
def if_edit_proc(request, pid):
    proc = process.objects.get(pk=pid)
    if request.user.id != proc.proc_author.id:
        try:
            if request.user.id != proc.proc_assigned.id:
                raise PermissionDenied
        except AttributeError:
            raise PermissionDenied
    task = tasks.objects.all().filter(
        tasks_proc_id=pid, tasks_is_deleted=False, tasks_tasks_id__isnull=True)
    if request.method == 'POST':
        file_form = FileForm(request.POST, request.FILES)
        proc_form = ProcessForm(request.POST, instance=proc)
        task_form = TaskFormPos(request.POST)
        if proc_form.is_valid() & file_form.is_valid():
            proc_form.save()
            for f in request.FILES.getlist('files_document'):
                newFile = files(files_document=f)
                newFile.files_proc_id = pid
                newFile.files_by_user_id = request.user.id
                newFile.files_name = f
                newFile.save()

            if 'save_process' in request.POST:
                return redirect('info_flow:if_show_proc', pid=pid)
            elif 'add_tasks' in request.POST:
                return redirect('info_flow:if_add_task', pid=pid)
    else:
        file_form = FileForm()
        fi = files.objects.all().filter(files_proc_id=pid)
        proc_form = ProcessForm(instance=proc)
        task_form = TaskFormPos(queryset=tasks.objects.none())
        users_with_perms = get_users_with_perms(
            proc).exclude(pk=proc.proc_author.id)
        users_list = User.objects.exclude(
            Q(pk__in=users_with_perms) | Q(pk=proc.proc_author.id))
        user_f = UsersFilter(request.GET, queryset=users_list)
        context = {'proc': proc, 'task': task, 'proc_form': proc_form, 'fi': fi, 'file_form': file_form,
                   'task_form': task_form, 'user_f': user_f, 'users_with_perms': users_with_perms}
        return render(request, 'info_flow/if_edit_proc.html', context)


@login_required
@permission_required('info_flow.change_tasks')
def if_edit_task(request, tid):
    task = tasks.objects.get(pk=tid)
    if not (request.user.id == task.tasks_proc.proc_author.id or request.user.id == task.tasks_author.id):
        if not (task.tasks_tasks_id != None and request.user.id == task.tasks_tasks.tasks_author.id):
            try:
                if not request.user in task.tasks_assigned.all():
                    raise PermissionDenied
            except AttributeError:
                raise PermissionDenied

    point = tasks.objects.all().filter(tasks_tasks_id=tid, tasks_is_deleted=False)
    if request.method == 'POST':
        file_form = FileForm(request.POST, request.FILES)
        task_form = TaskForm(request.POST, instance=task)
        point_form = TaskFormPointEdit(request.POST)
        if task_form.is_valid() & file_form.is_valid():
            task_form.save()
            for f in request.FILES.getlist('files_document'):
                newFile = files(files_document=f)
                newFile.files_tasks_id = tid
                newFile.files_by_user_id = request.user.id
                newFile.files_name = f
                newFile.save()
            if 'save_task' in request.POST:
                return redirect('info_flow:if_show_task', tid=tid)
            elif 'add_point' in request.POST:
                return redirect('info_flow:if_add_point', tid=tid)

    else:
        file_form = FileForm()
        fi = files.objects.all().filter(files_tasks_id=tid)
        task_form = TaskForm(instance=task)
        point_form = TaskFormPointEdit(queryset=tasks.objects.none())
        users_with_perms = get_users_with_perms(
            task).exclude(pk=task.tasks_author.id)
        users_list = User.objects.exclude(
            Q(pk__in=users_with_perms) | Q(pk=task.tasks_author.id))
        user_f = UsersFilter(request.GET, queryset=users_list)
        context = {'point': point, 'task': task, 'point_form': point_form, 'task_form': task_form,
                   'fi': fi, 'file_form': file_form, 'user_f': user_f, 'users_with_perms': users_with_perms}
    return render(request, 'info_flow/if_edit_task.html', context)


@login_required
@permission_required('info_flow.delete_process')
def if_delete_proc(request, proc_id, cat):
    delete_proc = process.objects.get(id=proc_id)
    if request.user.id != delete_proc.proc_author.id:
        raise PermissionDenied
    delete_proc.proc_is_deleted = True
    delete_proc.save()
    del_conn_com = comments.objects.filter(
        com_proc_id=proc_id).update(com_is_deleted=True)
    del_conn_task = tasks.objects.filter(
        tasks_proc_id=proc_id).update(tasks_is_deleted=True)
    deleted_files = files.objects.filter(
        files_proc_id=proc_id).update(files_is_deleted=True)
    return redirect('info_flow:if_processes', cat=cat, active='active')


@login_required
@permission_required('info_flow.add_tasks')
def if_add_point(request, tid):
    task = tasks.objects.get(pk=tid)
    if not (request.user.id == task.tasks_proc.proc_author.id or request.user.id == task.tasks_author.id):
        try:
            if not request.user in task.tasks_assigned.all():
                raise PermissionDenied
        except AttributeError:
            raise PermissionDenied
    if request.method == 'POST':
        point_form = TaskFormPoint(request.POST)
        if point_form.is_valid():
            for form in point_form:
                newPoint = form.save(commit=False)
                newPoint.tasks_proc_id = task.tasks_proc_id
                newPoint.tasks_is_active = True
                newPoint.tasks_tasks_id = tid
                newPoint.tasks_author_id = request.user.id
                newPoint.save()
                add_perms_to_new_object(request.user, newPoint, 'task')
            if 'save_process' in request.POST:
                return redirect('info_flow:if_processes', cat=process.objects.get(id=task.tasks_proc_id).proc_category, active='active')
            elif 'add_task' in request.POST:
                return redirect('info_flow:if_add_task', pid=task.tasks_proc_id)
        else:
            return redirect('info_flow:if_add_point', tid=tid)
    else:
        point_form = TaskFormPoint(queryset=tasks.objects.none())
        context = {'point_form': point_form, 'task': task}
        return render(request, 'info_flow/if_add_point.html', context)


@login_required
@permission_required('info_flow.view_posts')
def if_post_list(request):
    post_list = posts.objects.filter(posts_is_deleted=False).annotate(
        mess_temp=Max("messages")).order_by('-post_level', '-mess_temp', '-posts_created')
    posts_f = PostsFilter(request.GET, queryset=post_list)
    context = {'posts_f': posts_f}
    return render(request, 'info_flow/if_post_list.html', context)


@login_required
@permission_required('info_flow.add_posts')
def if_new_post(request):
    if request.method == 'POST':
        post_form = PostsForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)
        if post_form.is_valid() & file_form.is_valid():
            newPost = post_form.save(commit=False)
            newPost.posts_author = request.user
            newPost.save()
            for f in request.FILES.getlist('files_document'):
                newFile = files(files_document=f)
                newFile.files_posts_id = newPost.id
                newFile.files_by_user_id = request.user.id
                newFile.files_name = f
                newFile.save()

        return redirect('info_flow:if_post_list')
    else:
        file_form = FileForm()
        post_form = PostsForm()
        context = {'post_form': post_form, 'file_form': file_form}
        return render(request, 'info_flow/if_new_post.html', context)


@login_required
@permission_required('info_flow.view_posts')
def if_show_post(request, pid):
    post = posts.objects.get(pk=pid)
    fi = files.objects.all().filter(files_posts_id=pid)
    mess = messages.objects.all().filter(mess_posts_id=pid, mess_is_deleted=False)
    mess_form = MessageForm()
    if request.method == 'POST':
        messForm = MessageForm(request.POST)
        if messForm.is_valid():
            newMes = messForm.save(commit=False)
            newMes.mess_author = request.user
            newMes.mess_posts_id = pid
            newMes.save()
        return redirect('info_flow:if_show_post', pid=pid)

    context = {'post': post, 'mess': mess, 'mess_form': mess_form, 'fi': fi}
    return render(request, 'info_flow/if_show_post.html', context)


@login_required
@permission_required('info_flow.delete_messages')
def if_del_mess(request, mess_id):
    delete_mess = messages.objects.get(id=mess_id)
    if not request.user.id == delete_mess.mess_author.id:
        raise PermissionDenied
    postid = delete_mess.mess_posts_id
    delete_mess.mess_is_deleted = True
    delete_mess.save()
    return redirect('info_flow:if_show_post', pid=postid)


@login_required
@permission_required('info_flow.delete_posts')
def if_delete_post(request, post_id):
    delete_post = posts.objects.get(id=post_id)
    if not request.user.id == delete_post.posts_author.id:
        raise PermissionDenied
    delete_post.posts_is_deleted = True
    delete_post.save()
    del_conn_mess = messages.objects.all().filter(
        mess_posts_id=post_id).update(mess_is_deleted=True)
    deleted_files = files.objects.all().filter(
        files_posts_id=post_id).update(files_is_deleted=True)
    return redirect('info_flow:if_post_list')


@login_required
# @permission_required('info_flow.delete_posts')
def if_delete_com(request, object_type, e_id, com_id):
    delete_com = comments.objects.get(id=com_id)
    if not request.user.id == delete_com.com_author.id:
        raise PermissionDenied
    delete_com.com_is_deleted = True
    delete_com.save()
    if object_type == "proc":
        return redirect('info_flow:if_show_proc', pid=e_id)
    elif object_type == "task":
        return redirect('info_flow:if_show_task', tid=e_id)
    else:
        return redirect('info_flow:if_show_point', tid=e_id)


@login_required
@permission_required('info_flow.change_posts')
def if_edit_post(request, pid):
    post = posts.objects.get(pk=pid)
    if not request.user.id == post.posts_author.id:
        raise PermissionDenied
    if request.method == 'POST':
        post_form = PostsForm(request.POST, instance=post)
        file_form = FileForm(request.POST, request.FILES)
        if post_form.is_valid() & file_form.is_valid():
            post_form.save()
            for f in request.FILES.getlist('files_document'):
                newFile = files(files_document=f)
                newFile.files_posts_id = pid
                newFile.files_by_user_id = request.user.id
                newFile.files_name = f
                newFile.save()
        return redirect('info_flow:if_show_post', pid=pid)

    else:
        fi = files.objects.all().filter(files_posts_id=pid)
        file_form = FileForm()
        post_form = PostsForm(instance=post)
        context = {'post_form': post_form, 'post': post,
                   'file_form': file_form, 'fi': fi}
    return render(request, 'info_flow/if_edit_post.html', context)


@login_required
@permission_required('info_flow.view_files')
def download_file(request, fid):
    #############################################################################################
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
    delete_file = files.objects.get(id=file_id)
    if request.user.id != delete_file.files_proc.proc_author.id:
        try:
            if request.user.id != delete_file.files_proc.proc_assigned.id:
                raise PermissionDenied
        except AttributeError:
            raise PermissionDenied
    proc_id = delete_file.files_proc_id
    delete_file.delete()
    delete_file.delete_file()
    return redirect('info_flow:if_edit_proc', pid=proc_id)


@login_required
@permission_required('info_flow.delete_files')
def if_delete_post_file(request, file_id):
    delete_file = files.objects.get(id=file_id)
    if not request.user.id == delete_file.files_posts.posts_author.id:
        raise PermissionDenied
    post_id = delete_file.files_posts_id
    delete_file.delete()
    delete_file.delete_file()
    return redirect('info_flow:if_edit_post', pid=post_id)


@login_required
@permission_required('info_flow.delete_files')
def if_delete_task_file(request, file_id):
    delete_file = files.objects.get(id=file_id)
    if not (request.user.id == delete_file.files_tasks.tasks_proc.proc_author.id or request.user.id == delete_file.files_tasks.tasks_author.id):
        try:
            if not request.user in delete_file.files_tasks.tasks_assigned.all():
                raise PermissionDenied
        except AttributeError:
            raise PermissionDenied
    task_id = delete_file.files_tasks_id
    delete_file.delete()
    delete_file.delete_file()
    return redirect('info_flow:if_edit_task', tid=task_id)


@login_required
def user_profile(request, active):
    if active == "active":
        state = True
    else:
        state = False
    priv_proc = get_objects_for_user(request.user, 'info_flow.connect_proc', process.objects.all().filter(
        (Q(proc_author=request.user) | Q(proc_assigned_id=request.user)), proc_is_deleted=False, proc_is_active=state))
    filter_priv_proc = UserProcessFilter(request.GET, queryset=priv_proc)
    user_tasks = get_objects_for_user(request.user, 'info_flow.connect_task', tasks.objects.all(
    ).filter(tasks_assigned__pk=request.user.pk, tasks_is_deleted=False, tasks_is_active=state))
    #user_tasks=tasks.objects.all().filter(tasks_assigned__pk=request.user.pk, tasks_is_deleted=False, tasks_is_active=state)
    filter_tasks = UserTasksFilter(request.GET, queryset=user_tasks)
    context = {'user_tasks': user_tasks, 'priv_proc': priv_proc, 'state': state,
               'filter_priv_proc': filter_priv_proc, 'filter_tasks': filter_tasks}
    return render(request, 'info_flow/user_profile.html', context)


@login_required
@permission_required('info_flow.change_tasks')
def accept_task(request, task_id):
    tasks.toggle_active(task_id)
    task = tasks.objects.get(id=task_id)
    if task.tasks_tasks_id == None:
        if task.tasks_is_active == False:
            return redirect('info_flow:if_show_proc', pid=task.tasks_proc_id)
        else:
            return redirect('info_flow:if_show_task', tid=task.id)
    elif task.tasks_tasks_id != None:
        if task.tasks_is_active == False:
            return redirect('info_flow:if_show_task', tid=task.tasks_tasks_id)
        else:
            return redirect('info_flow:if_show_point', tid=task.id)


@login_required
@permission_required('info_flow.change_tasks')
def assign_task(request, object_type, task_id):
    us = request.user
    if tasks.objects.filter(pk=task_id, tasks_assigned__pk=us.pk).exists():
        ex = True
    else:
        ex = False
    redirect_id = tasks.set_assignation(task_id, us, ex, object_type)
    if object_type == "task":
        return redirect('info_flow:if_show_task', tid=redirect_id)
    elif object_type == "point":
        return redirect('info_flow:if_show_point', tid=redirect_id)


@login_required
@permission_required('info_flow.change_process')
def if_toggle_object_permission(request, user, object_id, object_type):
    user = User.objects.get(pk=user)
    if object_type == 'proc':
        perm_object = process.objects.get(pk=object_id)
        if not 'connect_proc' in get_perms(request.user, perm_object):
            raise PermissionDenied
    else:
        perm_object = tasks.objects.get(pk=object_id)
        if not 'connect_task' in get_perms(request.user, perm_object):
            raise PermissionDenied
    toggle_perm_on_object(user, perm_object, object_type)
    if object_type == 'proc':
        return redirect('info_flow:if_edit_proc', pid=object_id)
    elif object_type == 'task':
        return redirect('info_flow:if_edit_task', tid=object_id)


@login_required
@permission_required('info_flow.change_process')
@permission_required('info_flow.change_tasks')
def if_set_perms_to_all(request, proc_id):
    set_perm_to_subs(proc_id)
    return redirect('info_flow:if_edit_proc', pid=proc_id)


@login_required
@permission_required('info_flow.add_patterns')
def if_new_pattern(request, proc_id):
    if request.method == 'POST':
        pattern_form = PatternForm(request.POST)
        if pattern_form.is_valid():
            newPattern = pattern_form.save(commit=False)
            newPattern.pat_author = request.user
            newPattern.save()
            get_proc_elemenets(newPattern, proc_id, request.user)
            #create_proc_from_pattern(newPattern, request.user)
        return redirect('info_flow:if_show_proc', pid=proc_id)
    else:
        pattern_form = PatternForm()
        context = {'pattern_form': pattern_form, 'proc_id': proc_id}
    return render(request, 'info_flow/if_new_pattern.html', context)


@login_required
@permission_required('info_flow.view_patterns')
def if_patterns_list(request):
    if request.method == 'POST':
        new_pattern = CreateFromPattern(request.POST)
        p_id = request.POST.get("pattern_id")
        if new_pattern.is_valid():
            start = new_pattern.cleaned_data.get('start_date')
            end = new_pattern.cleaned_data.get('end_date')
            proc_id = create_proc_from_pattern(
                patterns.objects.get(pk=p_id), request.user, start, end)
            return redirect('info_flow:if_show_proc', pid=proc_id)

    patts = patterns.objects.all()
    new_pattern = CreateFromPattern()
    pattern_form = PatternForm()
    patterns_filter = PatternFilter(request.GET, queryset=patts)
    context = {'patterns_filter': patterns_filter,
               'new_pattern': new_pattern, 'pattern_form': pattern_form}
    return render(request, 'info_flow/if_patterns_list.html', context)


@login_required
@permission_required('info_flow.view_patterns')
def if_show_pattern(request, pat_id):
<<<<<<< HEAD
	patt=patterns.objects.get(pk=pat_id)
	pat_elements_proc=patterns_elements.objects.filter(pele_pattern=pat_id, pele_type=0)
	pat_elements_task=patterns_elements.objects.filter(pele_pattern=pat_id, pele_type=1)
	pat_elements_point=patterns_elements.objects.filter(pele_pattern=pat_id, pele_type=2)
	context={'pat_elements_proc':pat_elements_proc, 'pat_elements_task':pat_elements_task, 'pat_elements_point':pat_elements_point, 'pat_id':pat_id, 'patt':patt}
	return render(request, 'info_flow/if_show_pattern.html', context)
=======
    pat_elements_proc = patterns_elements.objects.filter(
        pele_pattern=pat_id, pele_type=0)
    pat_elements_task = patterns_elements.objects.filter(
        pele_pattern=pat_id, pele_type=1)
    pat_elements_point = patterns_elements.objects.filter(
        pele_pattern=pat_id, pele_type=2)
    context = {'pat_elements_proc': pat_elements_proc, 'pat_elements_task': pat_elements_task,
               'pat_elements_point': pat_elements_point, 'pat_id': pat_id}
    return render(request, 'info_flow/if_show_pattern.html', context)

>>>>>>> 5183a9dbb3bf9f7edd91d54e84118641e3562f65

@login_required
@permission_required('info_flow.change_patterns')
def if_edit_pattern(request, p_ele_id):
    p_element = patterns_elements.objects.get(pk=p_ele_id)
    if request.method == 'POST':
        edit_elem = Edit_pattern_elements(request.POST, instance=p_element)
        if edit_elem.is_valid():
            edit_elem.save()
            return redirect('info_flow:if_show_pattern', pat_id=p_element.pele_pattern.id)

    edit_elem = Edit_pattern_elements(instance=p_element)
    context = {'edit_elem': edit_elem, 'p_element': p_element}
    return render(request, 'info_flow/if_edit_pattern.html', context)


@login_required
@permission_required('info_flow.delete_patterns')
def if_delete_pattern(request, pat_id):
    del_pattern = patterns.objects.get(pk=pat_id)
    del_pattern.delete()
    return redirect('info_flow:if_patterns_list')


@login_required
@permission_required('info_flow.delete_patterns')
def if_delete_pattern_element(request, p_ele_id):
    del_pat_ele = patterns_elements.objects.get(pk=p_ele_id)
    del_pat_ele.delete()
    return redirect('info_flow:if_show_pattern', pat_id=del_pat_ele.pele_pattern.id)


@login_required
@permission_required('info_flow.change_patterns')
def if_edit_pattern_name(request, pat_id):
    cur_pat = patterns.objects.get(pk=pat_id)
    if request.method == 'POST':
        pattern_form = PatternForm(request.POST, instance=cur_pat)
        if pattern_form.is_valid():
            pattern_form.save()
        return redirect('info_flow:if_patterns_list')


@login_required
@permission_required('info_flow.change_patterns')
def if_change_pattern_element(request, p_ele_id):
    ele_cl = patterns_elements.objects.get(pk=p_ele_id)
    if ele_cl.pele_type == 0:
        number = patterns_elements.objects.filter(
            pele_pattern=ele_cl.pele_pattern, pele_type=1).count()
        save_pattern(pat_id=ele_cl.pele_pattern, pat_order=number+1, el_type=1,
                     el_name="Nowe zadanie", el_desc="Opis", el_proc=ele_cl.id)
    elif ele_cl.pele_type == 1:
        number = patterns_elements.objects.filter(
            pele_pattern=ele_cl.pele_pattern, pele_task=ele_cl.id, pele_type=2).count()
        save_pattern(pat_id=ele_cl.pele_pattern, pat_order=number+1, el_type=2,
                     el_name="Nowy punkt", el_desc="Opis", el_proc=ele_cl.pele_proc, el_task=ele_cl.id)

    return redirect('info_flow:if_show_pattern', pat_id=ele_cl.pele_pattern.id)
