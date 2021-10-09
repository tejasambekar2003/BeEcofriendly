from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
import datetime




class Drive(models.Model):
    host = models.ForeignKey(User, related_name="hostedBy", on_delete=PROTECT, null=True)
    members = models.ManyToManyField(User, related_name="mebers")
    drive_name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    target = models.IntegerField()
    desc = models.CharField(max_length=200, default="")

    def __str__(self):
        return f"{self.drive_name} : {self.location}"

# class Planter(models.Model):
#     planter = OneToOneField(User, on_delete=CASCADE, related_name="plantedBy")
#     drive_participated =  ForeignKey(Drive, on_delete=CASCADE, related_name="inDrives")

#     def __str__(self):
#         return f"{self.planter.first_name} : {self.planter.username}"




