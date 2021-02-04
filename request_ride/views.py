from django.shortcuts import render
from django.db import models
from login.models import Driver, Ride
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import dateparse


# Create your views here.
@login_required
def request_ride(request):
    if request.user.is_authenticated:
        return render(request, 'request_ride/request_ride.html', {})
    return


@login_required
def handle_request(request):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            if same_ride_checker(request.user, data['date_time'],  data['address']):
                print("Same ride exist!")
                return HttpResponseRedirect(reverse('main_page:main_pg'))
            can_share = data['share']
            departure_time = data['date_time']
            total_passenger_num = data['num_pass']
            destination = data['address']
            vehicle_type = data['vehicle_type']
            special_request = data['other']
            ride = Ride.objects.create(owner=request.user, can_share=can_share, departure_time=departure_time,
                                       total_passenger_num=total_passenger_num, status=0, destination=destination,
                                       vehicle_type=vehicle_type, special_request=special_request, sharer=[])
            ride.save()
            # request detail by ID
            return HttpResponseRedirect(reverse('request_ride:request_display', args=(ride.id, )))
        return render(request, 'request_ride/request_ride.html', {})
    else:
        return render(request, 'login/index.html', {'error_message': "Username not logged in."})


@login_required
def display_detail(request, ride_id):
    print("get in")
    if request.user.is_authenticated:
        try:
            ride = Ride.objects.get(pk=ride_id)
        except Ride.DoesNotExist:
            print("No ride exist.")
            return HttpResponseRedirect(reverse('main_page:main_pg'))
        else:
            # if the current user is neither the owen nor the sharer, he cannot view this detail
            if request.user != ride.owner and not is_sharer(request.user, ride):
                print("This ride does not belong to the owner")
                return HttpResponseRedirect(reverse('main_page:main_pg'))
            return render(request, 'request_ride/details.html', {'ride': ride, })
    else:
        return render(request, 'login/index.html', {'error_message': "Username not logged in."})


# check duplicate rides
def same_ride_checker(user, depart_time, destination):
    ride_list = Ride.objects.filter(owner_id=user.id)
    for ride in ride_list:
        format_time = str(dateparse.parse_datetime(depart_time)) + "+00:00"
        # print("date time = (", ride.departure_time, ", ", format_time, ")")
        # print("destination = (", ride.destination, ", ", destination, ")")
        if str(ride.destination) == destination and str(ride.departure_time) == format_time:
            return True
    return False


# iterating the sharer, checking user's identity
# return true if he is sharer, false otherwise
# Modified by yifan. user username to check
def is_sharer(user, ride):
    sharer_list = ride.sharer
    for sharer in sharer_list:
        if sharer == user.username:
            return True
    return False


@login_required
def edit(request):
    return render(request, 'request_ride/edit.html', {})

