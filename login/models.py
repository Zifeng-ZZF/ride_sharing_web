from django.db import models
from django.contrib.auth.models import User, Permission


# Create your models here.
# class User(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     is_driver = models.BooleanField(default = False)
#     email = models.CharField(max_length = 200)


class Driver(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    type = models.IntegerField()
    plate_num = models.CharField(max_length=50)
    capacity = models.IntegerField()


class Ride(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True)
    sharer = models.JSONField(blank=True, null=True)
    status = models.IntegerField()
    can_share = models.BooleanField(default=True)
    departure_time = models.DateTimeField()
    total_passenger_num = models.IntegerField()
    destination = models.CharField(max_length=200)
    vehicle_type = models.IntegerField()
    special_request = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        # 自定义的权限，两参数分别是权限的名字和权限的描述
        permissions = (
            ("isDriver", "search as driver"),
        )

