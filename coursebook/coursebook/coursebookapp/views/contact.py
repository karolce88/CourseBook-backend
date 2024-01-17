from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics


class ContactView(generics.ListCreateAPIView):
    template_name = "pages/contact.html"

    def get(self, request, *args, **kwargs):
        breadcrumbs = [
            ("Coursebook", reverse("home")),
            ("Kontakt", reverse("contact")),
        ]
        context = {
            "breadcrumbs": breadcrumbs,
        }
        return render(request, self.template_name, context)
