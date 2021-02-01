from django.shortcuts import render
from login.models import Driver, Ride
from django.contrib.auth.models import User, Permission
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse


# Create your views here.
def driver_access(request):
    user = request.user
    if user.is_authenticated:
        if user.has_perm('login.isDriver'):
            print("  ------------ has become driver")
            try:
                driver = Driver.objects.get(pk=user.id)
            except Driver.DoesNotExist:
                raise Http404("No driver information. contact IT: xxx@xx.com")
            confirmed_rides = Ride.objects.filter(driver=driver)
            context = {
                'driver': driver,
                'rides': confirmed_rides,
            }
            return render(request, 'driver_access/driver_access.html', context)
        return render(request, 'driver_access/driver_register.html', {})
    else:
        return render(request, 'login/index.html', {'error_message': "Username not logged in."})


# handle driver register form, process any invalid inputs if any
# create a driver and put into the DB if input is valid
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
    print("  ------------------  succesfully registered ... ")
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
