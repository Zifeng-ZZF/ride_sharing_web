from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from login.models import Driver, Ride
from django.db.models import Q


@login_required(login_url='login:index')
def my_ride(request, mode):
     if request.user.is_authenticated:
        all_rides_list = Ride.objects.order_by('departure_time').filter(Q(owner = request.user) | Q(sharer__has_any_keys=[request.user.username]))
        unconfirmed_rides_list = all_rides_list.filter(status = 0) 
        confirmed_rides_list = all_rides_list.filter(status = 1)
        finished_rides_list =all_rides_list.filter(status = 2)
        share_ride = Ride.objects.order_by('departure_time').filter(sharer__has_any_keys=[request.user.username]) 
        if mode == 0:
            ans = all_rides_list
        if mode == 1:
            ans = unconfirmed_rides_list
        if mode == 2:
            ans = confirmed_rides_list
        if mode == 3:
            ans = finished_rides_list
        if mode == 4:
            ans = share_ride
        return render(request, 'my_ride/my_ride.html', {'ans':ans})
     else:
        return render(request, 'login/index.html', {'message':"Please log in!"})
   