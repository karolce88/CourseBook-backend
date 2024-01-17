from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics

class AboutUsView(generics.ListCreateAPIView):
    template_name = "pages/about_us.html"

    def get(self, request, *args, **kwargs):
        breadcrumbs = [
            ("Coursebook", reverse("home")),
            ("O nas", reverse("about_us")),
        ]
        context = {
            "breadcrumbs": breadcrumbs,
        }
        return render(request, self.template_name, context)
