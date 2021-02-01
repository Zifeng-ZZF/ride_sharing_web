from django.urls import path
from . import views

app_name = 'driver_access'
urlpatterns = [
    path('', views.driver_access, name='driver_access'),
    path('register', views.handle_register_request, name='driver_reg'),
]