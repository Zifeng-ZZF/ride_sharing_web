from django.shortcuts import render


# Create your views here.
def request_ride(request):
    return render(request, 'request_ride/request_ride.html', {})