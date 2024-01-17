from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics

class FaqView(generics.ListCreateAPIView):
    template_name = "pages/faq.html"

    def get(self, request, *args, **kwargs):
        breadcrumbs = [
            ("Coursebook", reverse("home")),
            ("Faq", reverse("faq")),
        ]
        context = {
            "breadcrumbs": breadcrumbs,
        }
        return render(request, self.template_name, context)
