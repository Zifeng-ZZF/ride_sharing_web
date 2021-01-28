from django.shortcuts import render
from django.http import HttpResponse
from login.models import User

# Create your views here.
def main_page(request, user):
    context = {
        'username': user.user_name
    }
    return render(request, 'mainpage/main.html', context)
