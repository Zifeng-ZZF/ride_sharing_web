from django.urls import path
from . import views

app_name = 'request_ride'
urlpatterns = [
    path('<int:user_id>/', views.request_ride, name='request_ride'),
]