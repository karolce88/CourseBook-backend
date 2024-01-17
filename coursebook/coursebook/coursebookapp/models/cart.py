from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

from .course import Course


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    total_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"Koszyk użytkownika {self.user.username}"

    def calculate_total_price(self):
        cart_items = self.cartitem_set.all()
        total_price = Decimal("0.00")
        for cart_item in cart_items:
            total_price += cart_item.course.price * cart_item.quantity
        self.total_price = total_price
        self.save()
