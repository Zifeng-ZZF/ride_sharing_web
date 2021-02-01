from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import hashlib


# Create your views here.
def index(request):
    return render(request, 'login/index.html', {})
    
def register(request):
    return render(request, 'login/register.html', {})


# def setPassword(password):
#     md5 = hashlib.md5()
#     md5.update(password.encode(encoding='utf-8'))
#     password = md5.hexdigest()
#     return str(password)
    
        
def register_process(request):
    if request.method=="POST" and request.POST:
        data=request.POST
        username=data.get("username")
        email=data.get("email")
        password=data.get("password")
        existed_user = User.objects.filter(username = username)
        if(existed_user.count() > 0):
            return render(request, 'login/register.html', {'error_message': "Username has been used.",})   
        user = User.objects.create_user(username, email, password)
        user.save()
        message = "Register sucessfully!"
    return render(request, 'login/index.html', {'message': message})
    # return render(request, 'login/homepage.html', {'user':user})


def user_login(request):
     
    if request.method=="POST" and request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('login:homepage', args=()))
            # Redirect to a success page.
            
        else:
            # Return an 'invalid login' error message.
            message = 'Account does not exist！'
            return render(request, 'login/index.html', {'message': message})
    return render(request, 'login/index.html', {})
    
#if user is not validated, rediect to login_url
@login_required(redirect_field_name='next', login_url='login:index')
def homepage(request):
    return render(request, 'login/homepage.html', {'user':request.user})
    # if request.user.is_authenticated:
    #     return render(request, 'login/homepage.html', {'user':request.user})
    # else:
    #     return render(request, 'login/index.html', {})

