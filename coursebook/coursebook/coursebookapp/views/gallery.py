from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics


class GalleryView(generics.ListCreateAPIView):
    template_name = "pages/gallery.html"

    def get(self, request, *args, **kwargs):
        breadcrumbs = [
            ("Coursebook", reverse("home")),
            ("Galeria", reverse("gallery")),
        ]
        context = {
            "breadcrumbs": breadcrumbs,
        }
        return render(request, self.template_name, context)
