from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
import AccApp.views as views


app_name = 'AccApp'
urlpatterns = [
    path('login/', obtain_auth_token),
]
