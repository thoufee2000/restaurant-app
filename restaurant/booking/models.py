from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Table_detail(models.Model):

    table_name=models.CharField(max_length=10)
    table_capacity=models.IntegerField()
    booking_status = models.CharField(default="pending", max_length=30)

    def __str__(self):
        return self.table_name

class Table_booking(models.Model):
    TIME_SLOT_CHOICES = [
        ('12:00-1:00pm', '12:00-1:00 PM'),
        ('1:00-2:00pm', '1:00-2:00 PM'),
        ('2:00-3:00pm', '2:00-3:00 PM'),
        ('6:00-7:00pm', '6:00-7:00 PM'),
        ('7:00-8:00pm', '7:00-8:00 PM'),
        ('8:00-9:00pm', '8:00-9:00 PM'),
        ('9:00-10:00pm', '9:00-10:00 PM'),
        ('10:00-11:00pm', '10:00-11:00 PM'),
    ]

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    table=models.ManyToManyField(Table_detail)
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=50)
    phone = PhoneNumberField(region='IN')
    date=models.DateField()
    time=models.CharField(max_length=15,choices=TIME_SLOT_CHOICES)
    booked_date=models.DateTimeField(auto_now_add=True)
    booking_id=models.CharField(max_length=100,blank=True)
    payment_status = models.CharField(default="pending", max_length=30)


    def __str__(self):
        return self.user.username




class Payment_table(models.Model):
    name = models.CharField(max_length=50)
    amount = models.CharField(max_length=50)
    order_id = models.CharField(max_length=50, blank=True)
    razorpay_payment_id = models.CharField(max_length=50, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name
