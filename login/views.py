from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Create your views here.
def index(request):
    return render(request, 'login/index.html', {})


def register(request):
    return render(request, 'login/register.html', {})
    
        
def register_process(request):
    if request.method == "POST" and request.POST:
        data = request.POST
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        existed_user = User.objects.filter(username = username)
        if existed_user.count() > 0:
            message = "Username has been used."
            return render(request, 'login/register.html', {'message': message})
        user = User.objects.create_user(username, email, password)
        user.save()
        message = "Register sucessfully!"
    return render(request, 'login/index.html', {'message': message})
    # return render(request, 'login/homepage.html', {'user':user})


def user_login(request):
    if request.method == "POST" and request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('main_page:main_pg', args=()))
        else:
            # Return an 'invalid login' error message.
            message = 'Username/Password incorrect'
            return render(request, 'login/index.html', {'message': message})
    return render(request, 'login/index.html', {})


# if user is not validated, rediect to login_url
@login_required(redirect_field_name='next', login_url='login:index')
def homepage(request):
    return render(request, 'login/homepage.html', {'user': request.user})
