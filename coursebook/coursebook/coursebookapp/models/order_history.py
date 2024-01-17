from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .purchased_course import PurchasedCourse


class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchased_courses = models.ManyToManyField(PurchasedCourse)
    order_date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} ({self.order_date})"
