from django.shortcuts import render

# Create your views here.
def join_ride(request, user_id):
    return render(request, 'join_ride/join_ride.html', {})