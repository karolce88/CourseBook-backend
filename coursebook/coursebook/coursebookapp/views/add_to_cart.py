from rest_framework import generics

# from ..models import Course, Cart
from ..models import CartItem
from ..serializers import CartItemSerializer, CartSerializer
from rest_framework.response import Response
from rest_framework import status


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {"message": "Produkt został dodany do koszyka."}
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                "error": "Nie udało się dodać produktu do koszyka.",
                "details": serializer.errors,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class IncreaseCartItemQuantityView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def patch(self, request, *args, **kwargs):
        cart_item = self.get_object()
        serializer = self.get_serializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            if "quantity" in serializer.validated_data:
                new_quantity = serializer.validated_data["quantity"]
                if new_quantity > 0:
                    cart_item.quantity = new_quantity
                    cart_item.save()

                    updated_cart = cart_item.cart
                    updated_cart.calculate_total_price()
                    cart_serializer = CartSerializer(updated_cart)
                    return Response(cart_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"error": "Ilość nie może być ujemna."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"error": "Nieprawidłowy format danych."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
