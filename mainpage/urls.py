from django.urls import path
from . import views
from login.models import User

app_name = 'main_page'
urlpatterns = [
    path('<int:user_id>/', views.main_page, name='main_pg'),
    path('<int:user_id>/redirect', views.direct_func_buttons, name='redir'),
]