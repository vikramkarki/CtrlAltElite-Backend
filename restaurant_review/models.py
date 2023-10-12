from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name    


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.CharField(max_length=500)
    review_date = models.DateTimeField('review date')

    def __str__(self):
        return f"{self.restaurant.name} ({self.review_date:%x})"
 
class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    age = models.IntegerField()
    mobile_number = models.CharField(max_length=15)

class Therapist(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    address = models.TextField()

class Appointment(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist,on_delete=models.CASCADE)
    sc_checkin_time = models.DateTimeField()
    sc_checkout_time = models.DateTimeField()
    status = models.CharField(max_length=20)
    sos_flag = models.BooleanField()
    act_checkin_time = models.DateTimeField(blank=True)
    act_checkout_time = models.DateTimeField(blank=True)
 
class Admin(models.Model):
    name = models.CharField(max_length=100)