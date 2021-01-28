from django.shortcuts import render
from django.http import HttpResponse
from .models import User
import hashlib


# Create your views here.
def index(request):
    return render(request, 'login/index.html', {})
    
def register(request):
    return render(request, 'login/register.html', {})


def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode(encoding='utf-8'))
    password = md5.hexdigest()
    return str(password)
    
        
def register_process(request):
    if request.method=="POST" and request.POST:
        data=request.POST
        username=data.get("username")
        email=data.get("email")
        password=data.get("password")
        existed_user = User.objects.filter(username = username)
        if(existed_user.count() > 0):
            return render(request, 'login/register.html', {'error_message': "Username has been used.",})   
        user = User.objects.create(
            username=username,
            password=setPassword(password),
            email=email,
            
        )
        user.save()
    return render(request, 'login/homepage.html', {'user':user})


def login(request):
    if request.method=="POST" and request.POST:
        data=request.POST
        username=data.get("username")
        password=data.get("password")
        try:
            user = User.objects.get(username=username)
        except :
            error_message = 'Accout does not exist！'
            return render(request, 'login/index.html', {'error_message': error_message})
        existed_password = user.password
        md5 = hashlib.md5()
        md5.update(password.encode(encoding='utf-8'))
        password = md5.hexdigest()
        if password != existed_password:
            error_message = 'Wrong password！'
            return render(request, 'login/index.html', {'error_message': error_message})
           
    return render(request, 'login/homepage.html', {'user':user})
    

#def homepage(request, user_id):
    #user = get_object_or_404(User, pk=user_id)
    #return render(request, 'polls/detail.html', {'question': question})