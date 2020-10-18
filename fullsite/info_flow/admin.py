from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(process)
admin.site.register(tasks)
admin.site.register(comments)
admin.site.register(posts)
admin.site.register(category)
admin.site.register(messages)
admin.site.register(user_status)
admin.site.register(User, UserAdmin)
admin.site.register(Permission)

UserAdmin.fieldsets += ('Custom fields set', {'fields': ('user_is_balancing_unit', 'user_is_b_mesuring_unit', 'user_is_constracts_unit')}),