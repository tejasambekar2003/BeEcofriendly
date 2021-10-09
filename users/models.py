from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
import datetime


class Drive(models.Model):
    host = models.ForeignKey(User, related_name="hostedBy", on_delete=PROTECT, null=True)
    members = models.ManyToManyField(User, related_name="in_drives")
    drive_name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    target = models.IntegerField()
    desc = models.CharField(max_length=200, default="")
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.drive_name} : {self.location}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    location = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.user.first_name}"

class Tree(models.Model):
    drive = models.OneToOneField(Drive, on_delete=CASCADE)
    tree_count = models.IntegerField()
    def __str__(self):
        return f"{self.drive.drive_name} : {self.tree_count}"




class Post(models.Model):
    author = models.ForeignKey(User,null=True,  on_delete=CASCADE)
    drive = models.ForeignKey(Drive,null=True, on_delete=CASCADE)
    caption = models.CharField(default='', max_length=100, null=True)
    # date_posted = models.DateTimeField(default=datetime.datetime.now())
    image = models.ImageField(upload_to='images')

    def _str_(self):
        return str(self.pk)

