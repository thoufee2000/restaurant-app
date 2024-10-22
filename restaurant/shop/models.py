from django.db import models
from django.contrib.auth.models import User


class Dish(models.Model):
    name=models.CharField(max_length=50)
    desc=models.TextField()
    image=models.ImageField(upload_to='dishes',blank=True,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

