from django.shortcuts import render

# Create your views here.
def request_ride(request, user_id):
    return render(request, 'request_ride/request_ride.html', {})