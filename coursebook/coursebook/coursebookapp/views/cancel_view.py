from django.shortcuts import render
from rest_framework import generics


class CancelView(generics.ListCreateAPIView):
    template_name = "pages/cancel.html"

    def get(self, request, *args, **kwargs):
        del request.session["stripe_request_data"]
        context = {}
        return render(request, self.template_name, context)
