from django.urls import path
from . import views

app_name = 'driver_access'
urlpatterns = [
    path('', views.driver_access, name='driver_access'),
    path('register/', views.handle_register_request, name='driver_reg'),
    path('<int:ride_id>/detail/', views.handle_detail_form, name='detail_form_handle'),
    path('search/', views.on_search, name='on_search'),
    path('search/<int:ride_id>/claim/', views.handle_claim, name='claim_handle'),
    path('<int:ride_id>/complete/', views.on_complete, name='complete'),
]