from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(process)
admin.site.register(tasks)
admin.site.register(comments)
admin.site.register(posts)
admin.site.register(category)
admin.site.register(messages)
admin.site.register(user_status)
admin.site.register(user_profile)
