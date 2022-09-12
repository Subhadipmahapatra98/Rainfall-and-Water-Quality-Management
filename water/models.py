from pyexpat import model
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime
from django.conf import settings
from matplotlib.pyplot import cla
from matplotlib.style import available
from sklearn.metrics import mean_poisson_deviance

class User_details(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=12)
    address = models.CharField(max_length=12)

class Product(models.Model):
    quality = models.CharField(max_length=20)
    available = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    cost = models.CharField(max_length=10)
class NewOrder(models.Model):
    user = models.ForeignKey(User_details,on_delete=models.CASCADE)
    water = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.CharField(max_length=10)
    fullname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    pnum = models.CharField(max_length=12)
    pin = models.CharField(max_length=6)
    state = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    houseno = models.CharField(max_length=20)
    landmark = models.CharField(max_length=50)
    dated=models.DateTimeField(auto_now_add=True)
    expected_date = models.CharField(max_length=50)
    totalcost = models.CharField(max_length=50)
    confirmation = models.CharField(max_length=50)
    status = models.CharField(max_length=50)


class Querry(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=12)
    messages = models.CharField(max_length=1000)