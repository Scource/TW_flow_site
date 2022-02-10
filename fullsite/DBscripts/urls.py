from django.urls import path
from . import views


app_name = 'DBscripts'
urlpatterns = [
    path('scripts/peak_values', views.ScriptsView.as_view(),
         name='dbs_peak_values'),
    path('scripts/statuses', views.ScriptsView.as_view(),
        name='dbs_statuses'),
    path('scripts/check_node', views.ScriptsView.as_view(),
         name='dbs_check_node'),
    path('scripts/check_conf', views.ScriptsView.as_view(),
         name='dbs_check_conf'),
    path('scripts/get_PPE', views.ScriptsView.as_view(),
         name='dbs_get_PPE'),
    path('scripts/check_MB_PPE', views.ScriptsView.as_view(),
         name='dbs_check_MB_PPE'),
]
