from django.shortcuts import render
from rest_framework import generics
from ..models.cart import Cart
from ..serializers import OrderHistorySerializer
from django.shortcuts import get_object_or_404


class SuccessView(generics.ListCreateAPIView):
    template_name = "pages/success.html"
    serializer_class = OrderHistorySerializer

    def get(self, request, *args, **kwargs):
        stripe_request_data = request.session.get("stripe_request_data")

        serializer = self.get_serializer(
            data=stripe_request_data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            del request.session["stripe_request_data"]
        else:
            errors = serializer.errors

        user = request.user
        cart = Cart.objects.filter(user=user, is_completed=False).first()
        if cart:
            cart.delete()
            context = {}
        else:
            context = {}

        return render(request, self.template_name, context)
