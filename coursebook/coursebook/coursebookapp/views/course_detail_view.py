from django.shortcuts import render
from rest_framework import generics
from django.urls import reverse

from ..models.course import Course
from ..models.course_image import CourseImage
from ..serializers import CourseSerializer


class CourseDetailView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    lookup_field = "slug"
    template_name = "pages/course_detail.html"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        random_courses = Course.objects.order_by("?")[:6]

        instance.image = instance.courseimage_set.first()
        instance.images = CourseImage.objects.filter(course=instance)
        for course in random_courses:
            course.image = course.courseimage_set.first()

        breadcrumbs = [
            ("Coursebook", reverse("home")),
            (
                instance.province_slug,
                reverse(
                    "course_category", kwargs={"province_slug": instance.province_slug}
                ),
            ),
            (
                instance.title,
                reverse(
                    "course_detail",
                    kwargs={
                        "province_slug": instance.province_slug,
                        "slug": instance.slug,
                    },
                ),
            ),
        ]

        context = {
            "course": instance,
            "random_courses": random_courses,
            "breadcrumbs": breadcrumbs,
        }

        return render(request, self.template_name, context)
