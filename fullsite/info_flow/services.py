from .models import tasks, process, comments


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



# def tasks_in_proc_list(proc_list):
# 	for proc in proc_list:
# 		task=tasks.objects.all().filter(tasks_proc=proc.id, tasks_is_deleted=False, tasks_tasks_id__isnull=True)
# 		task_count=task.count()
# 		task_done=task.filter(tasks_is_active=False).count()
# 		proc.task_in = task_count
# 		proc.task_all = task_done
# 	return proc_list