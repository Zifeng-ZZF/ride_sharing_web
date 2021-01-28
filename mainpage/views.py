from django.shortcuts import render
from django.http import HttpResponse
from login.models import User

# Create your views here.
def main_page(request, user_id):
    try:
        logged_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return render(request, 'login/index.html', {'err_msg': "User not exist"})
    else:
        context = {
            'username': logged_user.user_name
        }
        return render(request, 'mainpage/main.html', context)
