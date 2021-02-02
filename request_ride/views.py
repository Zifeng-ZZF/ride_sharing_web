from django.shortcuts import render
from login.models import Driver, Ride
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse


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
            return render(request, 'request_ride/details.html', {'ride': ride})
        return render(request, 'request_ride/request_ride.html', {})
    else:
        return render(request, 'login/index.html', {'error_message': "Username not logged in."})


@login_required
def display_detail(request):
    return render(request, 'request_ride/details.html', {})