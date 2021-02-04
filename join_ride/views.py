from django.shortcuts import render
from django.db import models
from login.models import Driver, Ride
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import dateparse
from django.db.models import Q

class RequestInfo:
   searched_rides = None
   total_passenger_num = 0
   def __init__(self, searched_rides, total_passenger_num):
      self.searched_rides = searched_rides
      self.total_passenger_num = total_passenger_num
# Create your views here.
@login_required(login_url='login:index')
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
            
            return render(request, 'join_ride/search_result.html', {'ans':ride, 'p_num':total_passenger_num})

#process the join request. 
#Add username into Ride.sharer, ++passengernum
@login_required(login_url='login:index')
def request_process(request, ride_id, p_num):
    ride = Ride.objects.get(id = ride_id)
    sharer = ride.sharer
    sharer.append(request.user.username)
    ride.sharer = sharer
    ride.total_passenger_num = ride.total_passenger_num + p_num
    ride.save()
    return render(request, 'mainpage/main.html')

