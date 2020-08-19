from django.urls import path
from . import views



app_name='info_flow'
urlpatterns = [
    path('', views.index, name='if_index'),
    path('processes/', views.if_processes, name='if_processes'),
    path('processes/create', views.if_new_proc, name='if_new_proc'),
    path('processes/add_task/<int:pid>/', views.if_add_task, name='if_add_task'),
    path('processes/<int:pid>/', views.if_show_proc, name='if_show_proc'),
    path('processes/edit/<int:pid>/', views.if_edit_proc, name='if_edit_proc'),

    path('forum/', views.if_post_list, name='if_post_list'),
    path('forum/create', views.if_new_post, name='if_new_post'),
    path('forum/post/<int:pid>', views.if_show_post, name='if_show_post'),
    path('forum/post/edit/<int:pid>', views.if_edit_post, name='if_edit_post'),

    path('forum/post/if_add_message', views.if_add_message, name='if_add_message'),



    path('<int:fid>', views.download_file, name='download_file'),

 
]