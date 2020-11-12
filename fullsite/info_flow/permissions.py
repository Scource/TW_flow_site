from guardian.shortcuts import assign_perm, remove_perm, get_users_with_perms
from .models import process, tasks
from django.contrib.auth.models import Group

def add_perms_to_new_object(user, new_object, object_type):

	perms_dict={'proc':'connect_proc', 'task':'connect_task', 'point':'connect_point'}
	if object_type=='proc':
		if new_object.proc_is_private:
			assign_perm(perms_dict.get(object_type), user, new_object)
		else:
			set_perms_for_object(user, perms_dict.get(object_type), new_object)

	else:
		set_perms_for_object(user, perms_dict.get(object_type), new_object)


def set_perms_for_object(user, object_type, new_object):
	for g in user.groups.all():
		for user in g.user_set.all():
			assign_perm(object_type, user, new_object)



def toggle_perm_on_object(user, perm_object, object_type):
	perms_dict={'proc':'connect_proc', 'task':'connect_task', 'point':'connect_point'}
	if user.has_perm(perms_dict.get(object_type), perm_object):
		remove_perm(perms_dict.get(object_type), user, perm_object)
	else:
		assign_perm(perms_dict.get(object_type), user, perm_object)


def set_perm_to_subs(proc_id):
	proc=process.objects.get(pk=proc_id)
	users_with_perms_list=get_users_with_perms(proc, with_superusers=True)
	all_objects=tasks.objects.filter(tasks_proc=proc)

	for obj in all_objects:
		us_list=get_users_with_perms(obj)
		for us in us_list:
			remove_perm('connect_task', us, obj)
		for user in users_with_perms_list:
			assign_perm('connect_task', user, obj)
