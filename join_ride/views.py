from django.shortcuts import render
from django.db import models
from login.models import Driver, Ride
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import dateparse
from django.db.models import Q

# Create your views here.
def join_ride(request):
    return render(request, 'join_ride/join_ride.html', {'list':list})

#search the rides
@login_required(login_url='login:index')
def search(request):
    if request.POST:
            data = request.POST
            date_time_from = data['date_time_from']
            date_time_to = data['date_time_to']
            total_passenger_num = data['num_pass']
            destination = data['address']
            ride = Ride.objects.filter(Q(destination__icontains=destination) & Q(departure_time__range=(date_time_from, date_time_to)) & Q(status = 0))
            all_rides_list = Ride.objects.filter(Q(owner = request.user) | Q(sharer__has_any_keys=[request.user.username]))
            #rides, which user is already in, should not be displayed
            ride = ride.exclude(id__in=all_rides_list)
            return render(request, 'join_ride/search_result.html', {'ans':ride})

#process the join request. 
#Add username into Ride.sharer, ++passengernum
@login_required(login_url='login:index')
def request_process(request, ride_id):
    ride = Ride.objects.get(id = ride_id)
    sharer = ride.sharer
    sharer.append(request.user.username)
    ride.sharer = sharer
    ride.total_passenger_num = ride.total_passenger_num + 1
    ride.save()
    return render(request, 'mainpage/main.html')

