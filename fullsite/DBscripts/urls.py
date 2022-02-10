from django.urls import path
from . import views


app_name = 'DBscripts'
urlpatterns = [
    path('scripts/peak_values', views.Scripts.as_view(), name='dbs_script'),
]
