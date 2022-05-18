from django.urls import path
from . import views


app_name = 'BalancingMarket'
urlpatterns = [
    # Connections urls
    path('connection/', views.ConnList.as_view(), name='connection_list'),
    path('connection/<int:pk>/',
         views.ConnDetailView.as_view(), name='connection_detail'),
    path('connection/create/', views.ConnCreateView.as_view(),
         name='connection_form'),
    path('connection/<int:pk>/update/',
         views.ConnUpdateView.as_view(), name='connection_form_update'),
    path('connection/<int:pk>/delete/',
         views.ConnDeleteView.as_view(), name='connection_confirm_delete'),

     #elements urls
    path('element/POB/', views.ElementView.as_view(), name='element_list_POB'),
    path('element/SE/', views.ElementView.as_view(), name='element_list_SE'),
    path('element/<int:pk>/',
         views.ElementDetailView.as_view(), name='element_detail'),
    path('element/create/', views.ElementCreateView.as_view(), name='element_form'),
    path('element/<int:pk>/update/',
         views.ElementUpdateView.as_view(), name='element_form_update'),
    path('element/<int:pk>/delete/',
         views.ElementDeleteView.as_view(), name='element_confirm_delete'),

     #powerplants urls
    path('powerplant/', views.PowerPlantList.as_view(), name='powerplant_list'),
    path('powerplant/<int:pk>/',
         views.PowerPlantDetailView.as_view(), name='powerplant_detail'),
    path('powerplant/create/', views.PowerPlantCreateView.as_view(), name='powerplant_form'),
    path('powerplant/<int:pk>/update/',
         views.PowerPlantUpdateView.as_view(), name='powerplant_form_update'),
    path('powerplant/<int:pk>/delete/', views.PowerPlantDeleteView.as_view(), name='powerplant_confirm_delete'),

     # powerplants connections urls
    path('powerplant/connection/create/', views.PowerPlantConnectionCreateView.as_view(),
         name='powerplantconnection_form'),
    path('powerplant/connection/<int:pk>/update/',
         views.PowerPlantConnectionUpdateView.as_view(), name='powerplantconnection_form_update'),
    path('powerplant/connection/<int:pk>/delete/', views.PowerPlantConnectionDeleteView.as_view(),
         name='powerplantconnection_confirm_delete'),

     #files
    path('BM/dowlonad/<int:pk>/', views.DownloadFileView.as_view(),
         name='BM_download_file'),
    path('BM/file/delete/<int:pk>/', views.DeleteFileView.as_view(),
         name='BM_delete_file'),
]
