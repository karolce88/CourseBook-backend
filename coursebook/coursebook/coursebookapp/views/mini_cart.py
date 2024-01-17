from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..models import Cart
from ..serializers import CartSerializer
from django.contrib.auth.models import AnonymousUser


class MiniCartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer

    def get(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return Response(
                {
                    "message": "Dostęp zabroniony. Proszę się zalogować, aby zobaczyć koszyk."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {
                    "message": f"Koszyk dla użytkownika {request.user.email} nie istnieje."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        cart.calculate_total_price()
        serializer = self.serializer_class(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
