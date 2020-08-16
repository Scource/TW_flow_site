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


   
]