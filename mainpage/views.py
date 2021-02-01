from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User


# Create your views here.
def main_page(request):
    if request.user.is_authenticated:
        context = {}
        return render(request, 'mainpage/main.html', context)
    else:
        return render(request, 'login/index.html', {'error_message': "Username not logged in."})


# Listen on main page buttons and redirect them to different major functionalities
# passing user id to next pages
def direct_func_buttons(request):
    if request.user.is_authenticated:
        if request.GET.get('my_ride_btn'):
            return HttpResponseRedirect(reverse('my_ride:my_ride'))
        elif request.GET.get('request_ride_btn'):
            return HttpResponseRedirect(reverse('request_ride:request_ride'))
        elif request.GET.get('join_ride_btn'):
            return HttpResponseRedirect(reverse('join_ride:join_ride'))
        elif request.GET.get('driver_btn'):
            return HttpResponseRedirect(reverse('driver_access:driver_access'))
    else:
        return render(request, 'login/index.html', {'error_message': "Username not exist."})

