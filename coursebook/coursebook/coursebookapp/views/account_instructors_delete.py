from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from ..models.instructor import Instructor
from ..models.course import Course
from django.contrib import messages
from django.shortcuts import redirect


@method_decorator(login_required(login_url="login"), name="dispatch")
class AccountInstructorDelete(DeleteView):
    model = Instructor
    template_name = "pages/account-instructors.html"
    success_url = reverse_lazy("account_instructors")

    def form_valid(self, form):
        self.object = self.get_object()
        is_active_courses = Course.objects.filter(
            instructor=self.object, available=True
        )
        if is_active_courses.exists():
            messages.error(
                self.request,
                "Nie można usunąć instruktora, ponieważ jest przypisany do aktywnego kursu",
            )
            return redirect("account_instructors")
        else:
            response = super().form_valid(form)
            messages.success(self.request, "Prowadzący został usunięty")
            return response
