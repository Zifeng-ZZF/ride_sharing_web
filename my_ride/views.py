from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from login.models import Driver, Ride, Request
from django.db.models import Q


@login_required(login_url='login:index')
def my_ride(request, mode):
     if request.user.is_authenticated:
        request_list = Request.objects.filter(user = request.user)
        ride_list = []
        for ride_request in request_list:
            ride_list.append(ride_request.belong_to.id)
        all_rides_list = Ride.objects.order_by('-departure_time').filter(id__in = ride_list)
        unfinished_rides_list = all_rides_list.exclude(status = 3)
        unconfirmed_rides_list = unfinished_rides_list.filter(status = 0) 
        confirmed_rides_list = unfinished_rides_list.filter(status = 1)
        if mode == 0:
            ans = unfinished_rides_list
        if mode == 1:
            ans = unconfirmed_rides_list
        if mode == 2:
            ans = confirmed_rides_list
        return render(request, 'my_ride/my_ride.html', {'ans':ans})
     else:
        return render(request, 'login/index.html', {'message':"Please log in!"})
   