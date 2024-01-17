from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from django.contrib import messages

from ..models.instructor import Instructor
from ..serializers import InstructorSerializer
from ..helpers import check_membership

from django.http import JsonResponse


@method_decorator(login_required(login_url="login"), name="dispatch")
class AccountInstructorsView(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = InstructorSerializer
    template_name = "pages/account-instructors.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        isMember = check_membership(user)
        instructors = Instructor.objects.filter(app_user=user)
        context = {
            "user": user,
            "isMember": isMember,
            "instructors": instructors,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            messages.success(request, "Prowadzący został utworzony")
            return JsonResponse({"message": "Kurs został utworzony"}, status=200)
        else:
            messages.error(
                request, "Nie udało się utworzyć prowadzącego. Spróbuj ponownie"
            )
            errors = serializer.errors
            return JsonResponse(errors, status=400)

        # storage = get_messages(request)

        # return redirect("account_instructors")
        # return render(request, self.template_name, {"serializer": serializer})
