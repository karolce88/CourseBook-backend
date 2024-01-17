from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from ..models import Cart, CartItem
from ..serializers import CartSerializer, CartItemSerializer


class RemoveFromCartView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()

        if cart_item.cart.user != request.user:
            return Response(
                {"error": "Nie masz uprawnień do usunięcia tej pozycji z koszyka."},
                status=status.HTTP_403_FORBIDDEN,
            )

        cart = cart_item.cart
        cart_item.delete()

        serializer = CartSerializer(cart)
        cart.calculate_total_price()
        return Response(serializer.data)
