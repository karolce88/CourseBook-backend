from django.db import models
from .course import Course


class PurchasedCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Ordered: {self.course.title} ({self.quantity}x)"
