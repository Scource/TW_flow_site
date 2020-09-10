from django.urls import path
from . import views



app_name='info_flow'
urlpatterns = [
    path('', views.index, name='if_index'),
    path('processes/', views.if_processes, name='if_processes'),
    path('processes/create', views.if_new_proc, name='if_new_proc'),
    path('processes/add_task/<int:pid>/', views.if_add_task, name='if_add_task'),
    path('processes/task_<int:tid>/add_point/', views.if_add_point, name='if_add_point'),
    path('processes/<int:pid>/', views.if_show_proc, name='if_show_proc'),

    path('processes/edit/<int:pid>/', views.if_edit_proc, name='if_edit_proc'),
    path('processes/edit/task_<int:tid>/', views.if_edit_task, name='if_edit_task'),
    path('processes/show/task_<int:tid>/', views.if_show_task, name='if_show_task'),


    path('processes/delete/<int:proc_id>', views.if_delete_proc, name='if_delete_proc'),
    path('processes/edit/delete/<int:task_id>', views.if_delete_task, name='if_delete_task'),


    path('forum/', views.if_post_list, name='if_post_list'),
    path('forum/create', views.if_new_post, name='if_new_post'),
    path('forum/post/<int:pid>', views.if_show_post, name='if_show_post'),
    path('forum/post/edit/<int:pid>', views.if_edit_post, name='if_edit_post'),

    path('forum/post/delete/<int:mess_id>', views.if_del_mess, name='if_del_mess'),
    path('forum/delete/<int:post_id>', views.if_delete_post, name='if_delete_post'),



    path('<int:fid>', views.download_file, name='download_file'),
    path('processes/delete/file/<int:file_id>', views.if_delete_file, name='if_delete_file'),
    path('forum/delete/file/<int:file_id>', views.if_delete_post_file, name='if_delete_post_file'),
]
