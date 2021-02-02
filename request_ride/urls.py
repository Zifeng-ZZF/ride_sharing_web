from django.urls import path
from . import views

app_name = 'request_ride'
urlpatterns = [
    path('', views.request_ride, name='request_ride'),
    path('handle/', views.handle_request, name='request_handle'),
    path('<int:ride_id>/detail/', views.display_detail, name='request_display'),
    path('edit/', views.edit, name='edit'),
]