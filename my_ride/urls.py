from django.urls import path
from . import views

app_name = 'my_ride'
urlpatterns = [
    path('<int:user_id>/', views.my_ride, name='my_ride'),
]