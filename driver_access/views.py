from django.shortcuts import render

# Create your views here.
def driver_access(request, user_id):
    return render(request, 'driver_access/driver_access.html', {})