from .models import tasks, process, comments, category, patterns_elements
from .permissions import add_perms_to_new_object, toggle_perm_on_object
from django.db import models
import datetime
import calendar


def get_tasks_in_proc(pid):
	task=tasks.objects.all().filter(tasks_proc=pid, tasks_is_deleted=False)
	all_number=task.count()
	tasks_number=task.filter(tasks_tasks_id__isnull=True).count()
	points_number=task.filter(tasks_tasks_id__isnull=False).count()
	tasks_number_inactive=task.filter(tasks_tasks_id__isnull=True, tasks_is_active=False).count()
	points_number_active=task.filter(tasks_tasks_id__isnull=False, tasks_is_active=False).count()
	Dict = {'task':all_number, 'tasks_number':tasks_number , 'points_number':points_number, 
			'tasks_number_inactive':tasks_number_inactive, 'points_number_active':points_number_active}
	return Dict


def get_points_in_task(tid):
	task=tasks.objects.all().filter(tasks_tasks_id=tid, tasks_is_deleted=False)
	points_number=task.filter(tasks_tasks_id__isnull=False).count()
	points_number_inactive=task.filter(tasks_tasks_id__isnull=False, tasks_is_active=False).count()
	Dict = {'points_number':points_number, 'points_number_inactive':points_number_inactive}
	return Dict





def get_proc_elemenets(pat, proc_id, user):
	pro=process.objects.get(pk=proc_id)
	proc_pat=save_pattern(pat_id=pat, pat_order=1, el_type=0, el_name=pro.proc_process_name, el_desc=pro.proc_description)
	task_number=1
	for t in tasks.objects.filter(tasks_proc=proc_id, tasks_is_deleted=False, tasks_tasks_id__isnull=True):
		task_pat=save_pattern(pat_id=pat, pat_order=task_number, el_type=1, el_name=t.tasks_name, el_desc=t.tasks_description, el_proc=proc_pat)
		task_number+=1
		point_number=1
		for p in tasks.objects.filter(tasks_tasks=t.id, tasks_is_deleted=False):
			save_pattern(pat_id=pat, pat_order=point_number, el_type=2, el_name=p.tasks_name, el_desc=p.tasks_description, el_proc=proc_pat, el_task=task_pat)
			point_number+=1

def save_pattern(pat_id, pat_order, el_type, el_name, el_desc, el_proc=None, el_task=None):
	data_dict={
		'pele_pattern': pat_id,
		'pele_order': pat_order,
		'pele_type': el_type,
		'pele_name': el_name,
		'pele_desc' : el_desc,
		'pele_proc' : el_proc,
		'pele_task' : el_task}
	new_element_id=patterns_elements.save_pat_elements(data_dict)
	return new_element_id


def create_proc_from_pattern(pattern, user, start_date=None, end_date=None):

	proc_id=process_template_new(user, start_date, end_date, proc_data=patterns_elements.objects.get(pele_pattern=pattern.id, pele_type=0), pattern=pattern)
	add_perms_to_new_object(user, process.objects.get(pk=proc_id), 'proc')
	for t in patterns_elements.objects.filter(pele_pattern=pattern.id, pele_type=1).order_by('pele_order'):
		task_id=task_template_new(user, start_date, end_date, t.pele_name, t.pele_desc, proc_id)
		add_perms_to_new_object(user, tasks.objects.get(pk=task_id), 'task')
		for p in patterns_elements.objects.filter(pele_pattern=pattern.id, pele_type=2, pele_task=t.id).order_by('pele_order'):
			point_id=point_template_new(user, start_date, end_date, p.pele_name, p.pele_desc, proc_id, task_id)
			add_perms_to_new_object(user, tasks.objects.get(pk=point_id), 'task')
	return proc_id

def process_template_new(user, start_date, end_date, proc_data, pattern):
	data_dict={
		'proc_author':user,
		'proc_process_name': proc_data.pele_name,
		'proc_description' : proc_data.pele_desc,
		'proc_start_date' : start_date,
		'proc_end_date' : end_date,
		'proc_category' : pattern.pat_category,
		'proc_is_active':True,
		'proc_is_private':pattern.pat_is_private,
		'proc_is_deleted':False,
		'proc_assigned' : user}
	new_proc_id=process.save_proc_template(data_dict)
	return new_proc_id

def task_template_new(user, start_date, end_date, name, desc, proc_id):
	data_dict={
		'tasks_name':name,
		'tasks_author':user,
		'tasks_description':desc,
		'tasks_start_date':start_date,
		'tasks_end_date':end_date,
		'tasks_is_active':True,
		'tasks_is_deleted':False,
		'tasks_proc':process.objects.get(pk=proc_id)}
	new_task_id=tasks.save_task_template(data_dict)
	return new_task_id

def point_template_new(user, start_date, end_date, name, desc, proc_id, task_id):
	data_dict={
		'tasks_name':name,
		'tasks_author':user,
		'tasks_description':desc,
		'tasks_start_date':start_date,
		'tasks_end_date':end_date,
		'tasks_is_active':True,
		'tasks_is_deleted':False,
		'tasks_proc':process.objects.get(pk=proc_id),
		'tasks_tasks':tasks.objects.get(pk=task_id)}
	new_point_id=tasks.save_task_template(data_dict)
	return new_point_id




