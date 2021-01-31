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
        # code here ...
        if request.method == "POST" and request.POST:
            if Driver.objects.get(pk=user_id):
                print("User %d already has driver registration." % user_id)
                context = {'user': user, 'err_msg': "Already registered.", }
                return render(request, 'driver_access/driver_register.html', context)
            info = request.POST
            vtype = info['type_dropdown']
            plate_no = info['plate']
            cap = info['capacity']
            user.is_driver = True
            driver = Driver.objects.create(user=user, type=vtype, plate_num=plate_no, capacity=cap)
            driver.save()
            return render(request, 'driver_access/driver_access.html', {'user': user, })
        # .....
        context = {'user': user, 'err_msg': "No post data.", }
        return render(request, 'driver_access/driver_register.html', context)