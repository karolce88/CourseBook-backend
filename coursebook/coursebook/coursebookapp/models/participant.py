from django.db import models
from .purchased_course import PurchasedCourse


class Participant(models.Model):
    purchased_course = models.ForeignKey(PurchasedCourse, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"