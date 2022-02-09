from django.urls import path
from . import views


app_name = 'info_flow'
urlpatterns = [
    path('', views.index, name='if_index'),
    path('user/<str:active>', views.user_profile, name='user_profile'),

    path('processes/<str:cat>/<str:active>',
         views.if_processes, name='if_processes'),
    path('processes/', views.if_process_list, name='if_process_list'),
    path('processes/create/', views.if_new_proc, name='if_new_proc'),
    path('processes/add_task/<int:pid>/',
         views.if_add_task, name='if_add_task'),
    path('processes/task_<int:tid>/add_point/',
         views.if_add_point, name='if_add_point'),
    path('processes/show/<int:pid>/', views.if_show_proc, name='if_show_proc'),

    path('processes/edit/<int:pid>/', views.if_edit_proc, name='if_edit_proc'),
    path('processes/edit/task_<int:tid>/',
         views.if_edit_task, name='if_edit_task'),
    path('processes/show/task_<int:tid>/',
         views.if_show_task, name='if_show_task'),
    path('processes/show/task_<int:tid>/',
         views.if_show_task, name='if_show_point'),
    path('processes/change/task_<int:task_id>/',
         views.accept_task, name='accept_task'),
    path('processes/assign/<str:object_type>/task_<int:task_id>/',
         views.assign_task, name='assign_task'),


    path('processes/toggle_permissions/<int:user>/<int:object_id>/<str:object_type>',
         views.if_toggle_object_permission, name='if_toggle_object_permission'),
    path('processes/edit/set_perms_to_all/<int:proc_id>/',
         views.if_set_perms_to_all, name='if_set_perms_to_all'),

    path('processes/delete/<str:cat>/<int:proc_id>/',
         views.if_delete_proc, name='if_delete_proc'),
    path('processes/delete/<str:object_type>/<int:e_id>/<int:com_id>/',
         views.if_delete_com, name='if_delete_com'),
    path('processes/edit/delete/<int:task_id>/',
         views.if_delete_task, name='if_delete_task'),


    path('forum/', views.if_post_list, name='if_post_list'),
    path('forum/create', views.if_new_post, name='if_new_post'),
    path('forum/post/<int:pid>', views.if_show_post, name='if_show_post'),
    path('forum/post/edit/<int:pid>', views.if_edit_post, name='if_edit_post'),

    path('forum/post/delete/<int:mess_id>',
         views.if_del_mess, name='if_del_mess'),
    path('forum/delete/<int:post_id>',
         views.if_delete_post, name='if_delete_post'),

    path('pattern/new/<int:proc_id>', views.if_new_pattern, name='if_new_pattern'),
    path('pattern/show/<int:pat_id>',
         views.if_show_pattern, name='if_show_pattern'),
    path('pattern/list/', views.if_patterns_list, name='if_patterns_list'),
    path('pattern/show/edit/<int:p_ele_id>',
         views.if_edit_pattern, name='if_edit_pattern'),
    path('pattern/show/edit/pat/<int:pat_id>',
         views.if_edit_pattern_name, name='if_edit_pattern_name'),
    path('pattern/show/edit/add_element/<int:p_ele_id>',
         views.if_change_pattern_element, name='if_change_pattern_element'),
    path('pattern/show/delete/<int:pat_id>',
         views.if_delete_pattern, name='if_delete_pattern'),
    path('pattern/show/delete/element/<int:p_ele_id>',
         views.if_delete_pattern_element, name='if_delete_pattern_element'),


    path('download/file/id/<int:fid>', views.download_file, name='download_file'),
    path('processes/delete/file/<int:file_id>',
         views.if_delete_file, name='if_delete_file'),
    path('forum/delete/file/<int:file_id>',
         views.if_delete_post_file, name='if_delete_post_file'),
    path('processes/task/delete/file/<int:file_id>',
         views.if_delete_task_file, name='if_delete_task_file'),
]
