from django.urls import path
from . import views

app_name = 'join_ride'
urlpatterns = [
    path('<int:user_id>/', views.join_ride, name='join_ride'),
]