from django.db import models
from enum import Enum


class VehicleType(Enum):
    Sedan = 1,
    Coupe = 2,
    SportsCar = 3,
    SUV = 4,
    Minivan = 5,
    PickupTruck = 6,
    Hatchback = 7


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    is_driver = models.BooleanField(default = False)
    email = models.CharField(max_length = 200)


class Driver(models.Model):
    user = models.OneToOneField(User, primary_key = True, on_delete = models.CASCADE)
    type = models.IntegerField()
    plate_num = models.CharField(max_length=50)
    capacity = models.IntegerField()


class Ride(models.Model):
    owner = models.ForeignKey('User', on_delete = models.CASCADE)
    driver = models.ForeignKey('Driver', on_delete = models.CASCADE)
    sharer = models.IntegerField()
    status = models.IntegerField()
    can_share = models.BooleanField(default = True)
    departure_time = models.DateField()
    total_passenger_num = models.IntegerField()
    destination = models.CharField(max_length = 200)
    vehicle_type = models.IntegerField()
    special_request = models.CharField(max_length = 200)
