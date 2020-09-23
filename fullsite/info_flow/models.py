from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os

# Create your models here.

def user_directory_path(instance, filename):
	return 'user_files/{0}/{1}'.format(instance.files_by_user.username, filename)

	

class category(models.Model):
	cat_name =  models.CharField(max_length=20)
	cat_level = models.IntegerField()

	def __str__(self):
		return self.cat_name

class process(models.Model):
	proc_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET('deleted'), related_name='proc_user')
	proc_process_name = models.CharField(max_length=150)
	proc_description = models.TextField(null=True)
	proc_created = models.DateTimeField(auto_now_add=True)
	proc_modified = models.DateTimeField(auto_now=True)
	proc_start_date = models.DateTimeField(null=True, blank=True)
	proc_end_date = models.DateTimeField(null=True, blank=True)
	proc_category = models.ForeignKey(category, on_delete=models.CASCADE)
	proc_is_active=models.BooleanField(default=True)
	proc_is_private=models.BooleanField(default=False)
	proc_is_deleted=models.BooleanField(default=False)
	proc_assigned = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET('deleted'), null=True, blank=True, related_name='assigned_user')

	def __str__(self):
		return self.proc_process_name

	class Meta():
		ordering=['proc_created']
		permissions = (
		('check_proc', 'Check proc'),
		)

class tasks(models.Model):
	tasks_name = models.CharField(max_length=150, blank=False)
	tasks_description = models.TextField(null=True)
	tasks_created = models.DateTimeField(auto_now_add=True)
	tasks_modified = models.DateTimeField(auto_now=True)	
	tasks_start_date = models.DateTimeField(null=True, blank=True)
	tasks_end_date = models.DateTimeField(null=True, blank=True)
	tasks_assigned = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET('deleted'), null=True,  blank=True)
	tasks_is_active=models.BooleanField(default=True)
	tasks_is_deleted=models.BooleanField(default=False)
	tasks_proc=models.ForeignKey(process, on_delete=models.CASCADE)
	tasks_tasks=models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.tasks_name

	def toggle_active(task_id):
		task_status=tasks.objects.get(id=task_id)
		if task_status.tasks_is_active==True:
			task_status.tasks_is_active=False
		else:
			task_status.tasks_is_active=True
		task_status.save()


	def set_assignation(task_id, user):
		task_status=tasks.objects.get(id=task_id)
		task_status.tasks_assigned=user
		task_status.save()
		if task_status.tasks_tasks_id==None:
			return task_id
		else:
			return task_status.tasks_tasks_id

class comments(models.Model):
	com_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET('deleted'))
	com_body = models.TextField(null=True)
	com_created = models.DateTimeField(auto_now_add=True)
	com_modified = models.DateTimeField(auto_now=True)
	com_proc=models.ForeignKey(process, on_delete=models.CASCADE)
	com_is_deleted=models.BooleanField(default=False)

class posts(models.Model):
	posts_title=models.CharField(max_length=150)
	posts_author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET('deleted'))
	posts_created = models.DateTimeField(auto_now_add=True)
	posts_modified = models.DateTimeField(auto_now=True)
	posts_text=models.TextField()
	posts_is_deleted=models.BooleanField(default=False)
	post_level=models.IntegerField(default=0)

	def __str__(self):
		return self.posts_title

	class Meta():
		ordering=['-post_level', 'posts_modified']

class messages(models.Model):
	mess_author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET('deleted'))
	mess_created = models.DateTimeField(auto_now_add=True)
	mess_modified = models.DateTimeField(auto_now=True)
	mess_text=models.TextField()
	mess_is_deleted=models.BooleanField(default=False)
	mess_posts=models.ForeignKey(posts, on_delete=models.CASCADE)
	
class archive_posts(models.Model):
	arch_posts_title=models.CharField(max_length=150)
	arch_posts_author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET('deleted'))
	arch_posts_created = models.DateTimeField(auto_now_add=True)
	arch_posts_modified = models.DateTimeField(auto_now=True)
	arch_posts_text=models.TextField()
	arch_posts_is_deleted=models.BooleanField(default=False)


class user_status(models.Model):
	us_name=models.CharField(max_length=20)

class user_profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_department = models.CharField(max_length=100)
	user_profile_info = models.TextField()
	user_status = models.ForeignKey(user_status, on_delete=models.SET('deleted'))


class files(models.Model):
	files_name=models.CharField(max_length=300)
	files_added = models.DateTimeField(auto_now_add=True)
	files_by_user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	files_is_deleted=models.BooleanField(default=False)
	files_document = models.FileField(upload_to=user_directory_path, blank=True, null=True)#
	files_proc=models.ForeignKey(process, on_delete=models.CASCADE, blank=True, null=True)
	files_posts=models.ForeignKey(posts, on_delete=models.CASCADE, blank=True, null=True)
	files_tasks=models.ForeignKey(tasks, on_delete=models.CASCADE, blank=True, null=True)


	def delete_file(self, *args, **kwargs):
		os.remove(os.path.join(settings.MEDIA_ROOT, str(self.files_document)))
        

