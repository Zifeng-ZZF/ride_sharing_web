from django.shortcuts import render
from login.models import User,Driver,Ride
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def driver_access(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return render(request, 'login/index.html', {'error_message': "Username not exist."})
    else:
        if user.is_driver:
            return render(request, 'driver_access/driver_access.html', {'user': user, })
        # open registration page directly
        return render(request, 'driver_access/driver_register.html', {'user': user, })


# handle driver register form, process any invalid inputs if any
# create a driver and put into the DB if input is valid
def handle_register_request(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return render(request, 'login/index.html', {'error_message': "Username not exist."})
    else:
        context = {
            'user': user,
            'err_msg': "",
            'err_vtype': False,
            'err_plate': False,
            'err_cap': False,
        }
        if request.method == "POST" and request.POST:
            if request.POST.get('cancel'):  # if cancel, go back to main page
                return HttpResponseRedirect(reverse('main_page:main_pg', args=user_id))
            valid_info = check_valid(context, request.POST)  # checking validity of form input
            context = valid_info[0];
            has_err = valid_info[1];
            if has_err:
                return render(request, 'driver_access/driver_register.html', context)
            if Driver.objects.filter(pk=user_id).count() > 0:  # checking user's register record
                context['err_msg'] = "Already registered."
                return render(request, 'driver_access/driver_register.html', context)
            info = request.POST  # correct input, save to database
            driver = Driver.objects.create(user=user, type=info['vehicle_type'],
                                           plate_num=info['plate'], capacity=info['capacity'])
            driver.save()
            user.is_driver = True  # also update user table information
            user.save()
            return render(request, 'driver_access/driver_access.html', {'user': user, })
        return render(request, 'driver_access/driver_register.html', context)


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
    if capacity:
        if not capacity.isdigit() or int(capacity) < 0:
            context['err_cap'] = True
            has_err = True
    return context, has_err
