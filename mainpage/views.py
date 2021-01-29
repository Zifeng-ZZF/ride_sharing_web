from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from login.models import User

# Create your views here.
def main_page(request, user_id):
    # redirect to login if try to access directly
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return render(request, 'login/index.html', {'error_message': "Username not exist."})
    else:
        context = {
            'user': user
        }
        return render(request, 'mainpage/main.html', context)


def direct_func_buttons(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return render(request, 'login/index.html', {})
    else:
        if request.GET.get('my_ride_btn'):
            return HttpResponseRedirect(reverse('my_ride:my_ride', args = (user_id,)))
        elif request.GET.get('request_ride_btn'):
            return HttpResponseRedirect(reverse('request_ride:request_ride', args = (user_id,)))
        elif request.GET.get('join_ride_btn'):
            return HttpResponseRedirect(reverse('join_ride:join_ride', args = (user_id,)))
        elif request.GET.get('driver_btn'):
            return HttpResponseRedirect(reverse('driver_access:driver_access', args = (user_id,)))

