from . import views
from django.urls import path
from login.models import User

app_name = 'main_page'
urlpatterns = [
    path('', views.main_page, name='main_pg'),
    path('redirect/', views.direct_func_buttons, name='redir'),
]