from django.shortcuts import render, redirect
from django.contrib import messages

from rest_framework import generics

from ..serializers import AppUserSerializer


class RegisterView(generics.ListCreateAPIView):
    serializer_class = AppUserSerializer
    template_name = ""

    def get(self, request, *args, **kwargs):
        self.template_name = self.get_template_name_from_url(request)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            messages.success(request, "Rejestracja przebiegła pomyślnie")
            return redirect("account")
        else:
            messages.error(
                self.request, "Nie udało się utworzyć konta. Spróbuj ponownie"
            )
            return redirect(request.path)
            # return render(request, self.template_name, {"serializer": serializer})

    def get_template_name_from_url(self, request):
        url = request.path
        template_name = (
            "register-customer.html"
            if "register-customer" in url
            else "register-company.html"
        )
        return "pages/" + template_name
