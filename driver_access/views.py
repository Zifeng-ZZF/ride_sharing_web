from django.shortcuts import render
from login.models import Driver, Ride, Request
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse


# driver access view, if user is driver and possess the drive, detail
# of vehicle info and list of rides will be presented
@login_required
def driver_access(request):
    user = request.user
    if user.is_authenticated:
        if user.has_perm('login.isDriver'):
            try:
                driver = Driver.objects.get(pk=user.id)
            except Driver.DoesNotExist:
                raise Http404("No driver information. contact IT: xxx@xx.com")
            confirmed_rides = Ride.objects.filter(driver=driver)
            context = {
                'driver': driver,
                'rides': list(confirmed_rides),
            }
            return render(request, 'driver_access/driver_access.html', context)
        return render(request, 'driver_access/driver_register.html', {})
    return render(request, 'login/index.html', {'error_message': "Username not logged in."})


# handle driver register form, process any invalid inputs if any
# create a driver and put into the DB if input is valid
@login_required
def handle_register_request(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, 'login/index.html', {'error_message': "Username not logged in."})
    context = {
        'user': user,
        'err_msg': "",
        'err_vtype': False,
        'err_plate': False,
        'err_cap': False,
    }
    if request.method == "POST" and request.POST:
        return handle_register_data(request, context, user)
    return render(request, 'driver_access/driver_register.html', context)


# process form data
def handle_register_data(request, context, user):
    if request.POST.get('cancel'):  # if cancel, go back to main page
        return HttpResponseRedirect(reverse('main_page:main_pg'))
    data = request.POST
    valid_info = check_valid(context, data)  # checking validity of form input
    context = valid_info[0];
    has_err = valid_info[1];
    if has_err:
        return render(request, 'driver_access/driver_register.html', context)
    if user.has_perm('isDriver') or Driver.objects.filter(user_id=user.id).count() > 0:
        context['err_msg'] = "You are already a driver."
        return render(request, 'driver_access/driver_register.html', context)
    driver = Driver.objects.create(user=user, type=data['vehicle_type'], plate_num=data['plate'],
                                   capacity=data['capacity'])
    perm = Permission.objects.get(codename='isDriver')
    user.user_permissions.add(perm)  # grant permission after registering
    user.save()
    driver.save()
    return HttpResponseRedirect(reverse('driver_access:driver_access'))


# checking form input validity and set err flags
# return new context info and overall err status
def check_valid(context, data):
    has_err = False
    vehicle = data['vehicle_type']
    plate = data['plate']
    capacity = data['capacity']
    if int(vehicle) == 10:
        context['err_vtype'] = True
        has_err = True
    if plate:
        for c in plate:
            if not c.isdigit() and not c.isalpha():
                context['err_plate'] = True
                has_err = True
                break
        if Driver.objects.filter(plate_num=plate).count() > 0:
            context['err_plate_num'] = 'The plate has already been registered.'
            has_err = True
    if capacity:
        if not capacity.isdigit() or int(capacity) < 0:
            context['err_cap'] = True
            has_err = True
    return context, has_err


# enter search page and render search page by listing all rides that the
# driver is the current user
@login_required
def on_search(request):
    if request.user.is_authenticated:
        user = request.user
        driver = Driver.objects.get(pk=user)
        open_rides_list = validate_rides(driver, user)
        context = {
            'driver': driver,
            'rides': open_rides_list,
        }
        return render(request, 'driver_access/driver_search.html', context)
    return HttpResponseRedirect(reverse('driver_access:driver_access'))


# filtering rides that meet the driver's vehicle type, capacity
# and the ride must be "open" and has no driver yet
# the driver can't be the owner or the sharer
def validate_rides(driver, user):
    open_rides = Ride.objects.filter(status=0, vehicle_type=driver.type, total_passenger_num__lte=driver.capacity,
                                     driver=None)
    open_rides = open_rides.exclude(owner=user)
    open_list = []
    for ride in open_rides:
        if user.username not in ride.sharer:
            open_list.append(ride)
    return open_list


# handle claim request from driver who pick a ride to confirm
# change the ride status and notify participants via email
@login_required
def handle_claim(request, ride_id):
    if request.user.is_authenticated:
        user = request.user
        ride = Ride.objects.get(pk=ride_id)
        ride.status = 1
        ride.driver = Driver.objects.get(pk=user)
        ride.save()
        ride_request = Request.objects.create(user=request.user, role=2, belong_to=ride, passenger_num=0)
        ride_request.save()
        print("-------------- successfully claimed: ", ride_id)
        # return to the page with refreshed list
        return HttpResponseRedirect(reverse('driver_access:on_search'))
    return render(request, 'login/index.html', {'error_message': "Username not logged in."})


# on click of driver's own rides and display the details
# listing sharers information and pass to template
@login_required
def handle_detail_form(request, ride_id):
    if request.user.is_authenticated:
        print("Handling detail form click on ride: ", ride_id)
        ride = Ride.objects.get(pk=ride_id)
        sharers = []
        sharers_names = list(ride.sharer)
        for name in sharers_names:
            temp = User.objects.get(username=name)
            sharers.append(temp)
        context = {
            'ride': ride,
            'sharers': sharers,
        }
        return render(request, 'request_ride/details.html', context)
    return render(request, 'login/index.html', {'error_message': "Username not logged in."})


# on complete the ride, notify all the participants the ride is complete via email
@login_required
def on_complete(request, ride_id):
    print("Complete a ride !!! : ", ride_id)
    ride = Ride.objects.get(pk=ride_id)
    # delete all requests related to the ride
    Request.objects.filter(belong_to=ride).delete()
    return render(request, 'driver_access/driver_access.html')