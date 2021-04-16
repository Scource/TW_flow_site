"""
 RB_mgmt urls
"""

from django.urls import path
import RB_mgmt.views as views


app_name = 'RB_mgmt'
urlpatterns = [
    path('connection/', views.ConnList.as_view()),
    path('connection/create/', views.ConnCreateView.as_view()),
    path('connection/<int:pk>/edit/', views.ConnUpdateView.as_view()),
    path('connection/<int:pk>/delete/', views.ConnDeleteView.as_view()),

    path('element/<str:type>/', views.ElementList.as_view()),
    path('element/create/', views.ElementCreateView.as_view()),
    path('element/<int:pk>/edit/', views.ElementUpdateView.as_view()),
    path('element/<int:pk>/delete/', views.ElementDeleteView.as_view()),

    path('powerplant/', views.PowerPlantList.as_view()),
    path('powerplant/create/', views.PowerPlantCreateView.as_view()),
    path('powerplant/<int:pk>/edit/', views.PowerPlantUpdateView.as_view()),
    path('powerplant/<int:pk>/delete/', views.PowerPlantDeleteView.as_view()),

    path('powerplant/connection/', views.PowerPlantConnectionList.as_view()),

]
