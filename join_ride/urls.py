from django.urls import path
from . import views

app_name = 'join_ride'
urlpatterns = [
    path('', views.join_ride, name='join_ride'),
    path('search/', views.search, name='search'),
    path('<int:ride_id>/<int:p_num>/request_process/', views.request_process, name='request_process'),
]