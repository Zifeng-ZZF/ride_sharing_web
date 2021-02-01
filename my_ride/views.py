from django.shortcuts import render

# Create your views here.
def my_ride(request, user_id):
    return render(request, 'my_ride/my_ride.html', {})