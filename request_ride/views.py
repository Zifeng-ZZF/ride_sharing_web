from django.shortcuts import render
from django.db import models
from login.models import Driver, Ride, Request
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import dateparse
from django.core.mail import send_mail, BadHeaderError, send_mass_mail
from smtplib import SMTPException, SMTPRecipientsRefused


# Create your views here.
@login_required
def request_ride(request):
    if request.user.is_authenticated:
        return render(request, 'request_ride/request_ride.html', {})
    return render(request, 'login/index.html', {'error_message': "Username not logged in."})


# handling request for a ride, process the request form, and create corresponding ride and owner request
@login_required
def handle_request(request):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            if same_ride_checker(request.user, data['date_time'],  data['address']):
                return render(request, 'request_ride/request_ride.html', {'err_msg': "Same request has been created!!!!"})
            can_share = data['share']
            departure_time = data['date_time']
            total_passenger_num = data['num_pass']
            destination = data['address']
            vehicle_type = data['vehicle_type']
            special_request = data['other']
            ride = Ride.objects.create(owner=request.user, can_share=can_share, departure_time=departure_time,
                                       total_passenger_num=total_passenger_num, status=0, destination=destination,
                                       vehicle_type=vehicle_type, special_request=special_request, sharer=[])
            ride_request = Request.objects.create(user=request.user, role=0, belong_to=ride,
                                                  passenger_num=total_passenger_num)
            ride_request.save()
            ride.save()
            return HttpResponseRedirect(reverse('request_ride:request_display', args=(ride.id, )))
        return render(request, 'request_ride/request_ride.html', {})
    return render(request, 'login/index.html', {'error_message': "Username not logged in."})


# handling request for displaying the detail of the ride request
@login_required
def display_detail(request, ride_id):
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
            request_list = []
            for name in ride.sharer:
                temp = User.objects.get(username=name)
                request_temp = Request.objects.get(user=temp, belong_to=ride)
                request_list.append(request_temp)
            context = {
                'ride': ride,
                'requests': request_list,
            }
            return render(request, 'request_ride/details.html', context)
    return render(request, 'login/index.html', {'error_message': "Username not logged in."})


# check duplicate rides
def same_ride_checker(user, depart_time, destination):
    ride_list = Ride.objects.filter(owner_id=user.id)
    for ride in ride_list:
        format_time = str(dateparse.parse_datetime(depart_time)) + "+00:00"
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


# on entering edit pages, based on role of request to show different options to edit
@login_required
def edit(request, ride_id):
    if request.user.is_authenticated:
        ride = Ride.objects.get(pk=ride_id)
        if ride.status == 2:
            return HttpResponseRedirect(reverse('main_page:main_pg'))
        ride_request = Request.objects.get(user=request.user, belong_to=ride)
        context = {
            'ride': ride,
            'request': ride_request,
        }
        return render(request, 'request_ride/edit.html', context)
    return render(request, 'login/index.html', {'error_message': "Username not logged in."})


# on save edit changes, update corresponding data in the database based on the request role
# owner/sharer update info, driver complete the tasks
@login_required
def handle_edit(request, request_id):
    if request.user.is_authenticated:
        ride_request = Request.objects.get(pk=request_id)
        ride = Ride.objects.get(pk=ride_request.belong_to.id)
        if request.POST:
            data = request.POST
            if ride_request.role == 0:
                owner_edit_save(ride, ride_request, data)
            elif ride_request.role == 1:
                ride.can_share = data['share']
                ride.save()
            elif ride_request.role == 2:
                return HttpResponseRedirect(reverse('driver_access:complete', args=(ride.id, )))
        return render(request, 'request_ride/details.html', {'ride': ride, 'request': ride_request, })
    return render(request, 'login/index.html', {'error_message': "Username not logged in."})


# if owner edit and save changes, need to deal with sharer
def owner_edit_save(ride, ride_request, data):
    need_delete = False
    old_dest = ""
    old_datetime = None;
    if ride.destination != data['dest'] or ride.departure_time != data['date_time']:
        old_dest = ride.destination
        old_datetime = ride.departure_time
        need_delete = True
    ride.destination = data['dest']
    ride.departure_time = data['date_time']
    ride.vehicle_type = data['vehicle_type']
    ride.special_request = data['special']
    ride.total_passenger_num -= ride_request.passenger_num;
    ride.total_passenger_num += int(data['pass'])
    ride.can_share = data['share']
    # update request
    ride_request.passenger_num = int(data['pass'])
    if need_delete:
        handle_need_delete(ride, old_dest, old_datetime)
    ride.save()
    ride_request.save()
    Request.objects.filter(belong_to=ride, role=1).delete()
    pass


# if destination or date changes, all the sharer need to be removed from the ride
# their requests are accordingly removed, and the sharer list is cleared
# email notification will be sent
def handle_need_delete(ride, old_dest, old_datetime):
    sharer_list = ride.sharer
    for sharer_name in sharer_list:
        sharer = User.objects.get(username=sharer_name)
        sharer_request = Request.objects.get(user=sharer, belong_to=ride)
        ride.total_passenger_num -= sharer_request.passenger_num
    ride.sharer = []
    # emailing
    subject = "Canceled/Modified ride"
    content = "Your original ride to " + old_dest + " at " + str(old_datetime) + " is canceled."
    data_list = []
    if len(sharer_list) > 0:
        for sharer_name in sharer_list:
            temp_tuple = (subject, content, None, [User.objects.get(username=sharer_name).email])
            data_list.append(temp_tuple)
        try:
            send_mass_mail(data_list, fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        except SMTPException as e:
            print(e)

