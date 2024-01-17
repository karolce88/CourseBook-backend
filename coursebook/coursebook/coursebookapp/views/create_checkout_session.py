from django.conf import settings
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
import stripe
import json

from ..models.cart import Cart
from ..models.cart_item import CartItem

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSession(generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user, is_completed=False).first()
        cart_items = CartItem.objects.filter(cart=cart)

        cart_items_data = []
        course_info = []
        for cart_item in cart_items:
            item_data = {
                "price_data": {
                    "currency": "pln",
                    "product_data": {
                        "name": cart_item.course.title,
                    },
                    "unit_amount": int(cart_item.course.price * 100),
                },
                "quantity": cart_item.quantity,
            }
            cart_items_data.append(item_data)
            course_info.append(
                {
                    "course_id": cart_item.course.id,
                    "seats_purchased": cart_item.quantity,
                }
            )

        session = stripe.checkout.Session.create(
            # success_url="http://127.0.0.1:8000/payment/success/{CHECKOUT_SESSION_ID}",
            # cancel_url="http://127.0.0.1:8000/payment/failed/{CHECKOUT_SESSION_ID}",
            success_url=f"{settings.WEB_URL}payment/success/{{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.WEB_URL}payment/failed/{{CHECKOUT_SESSION_ID}}",
            payment_method_types=["card", "blik"],
            line_items=cart_items_data,
            mode="payment",
            submit_type="auto",
            metadata={
                "course_info": json.dumps(course_info),
            },
        )

        request.session["stripe_request_data"] = request.data

        return JsonResponse({"id": session.id})
