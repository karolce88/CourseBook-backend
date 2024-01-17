from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics
from django.core.paginator import Paginator

from ..models.course import Course


class NewestView(generics.ListCreateAPIView):
    template_name = "pages/newest.html"
    default_page_size = 6

    def get(self, request, *args, **kwargs):
        newest_courses = Course.objects.filter(available=True).order_by("-id")[:12]

        for course in newest_courses:
            image = course.courseimage_set.first()
            course.image = image

        paginator = Paginator(newest_courses, self.default_page_size)
        page_number = request.GET.get("page")
        paginated_courses = paginator.get_page(page_number)

        breadcrumbs = [
            ("Coursebook", reverse("home")),
            ("Nowości", reverse("newest")),
        ]

        context = {
            "breadcrumbs": breadcrumbs,
            "courses":paginated_courses,
        }
        return render(request, self.template_name, context)
