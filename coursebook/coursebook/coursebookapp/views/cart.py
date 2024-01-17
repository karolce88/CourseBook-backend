from rest_framework import generics
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from rest_framework import generics

from ..models.cart import Cart
from ..models.cart_item import CartItem

from ..serializers import CartSerializer


@method_decorator(login_required(login_url="login"), name="dispatch")
class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    template_name = "pages/cart.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user, is_completed=False).first()
        cart_items = CartItem.objects.filter(cart=cart)

        context = {
            "user": user,
            "cart": cart,
            "cart_items": cart_items,
        }

        return render(request, self.template_name, context)
