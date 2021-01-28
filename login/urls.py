from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    #/login/     used for login  
    path('', views.index, name = 'index'),
    #/login/register/     used for register  
    path('register/', views.register, name = 'register'),
    #/login/register/     used for register  
    path('register_process/', views.register_process, name = 'register_process'),
    path('user_login/', views.login, name = 'user_login'),
    #/login/homepage/     test homepage  
    #path('homepage/', views.homepage, name = 'homepage'),
    
]