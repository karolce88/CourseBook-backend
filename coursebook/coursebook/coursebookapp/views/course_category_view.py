from django.shortcuts import render
from django.urls import reverse
from django.urls import resolve
from django.core.paginator import Paginator
from rest_framework import generics

from ..models.course import Course
from ..serializers import CourseSerializer


class CourseCategoryView(generics.ListAPIView):
    serializer_class = CourseSerializer
    template_name = "pages/course-category.html"
    default_page_size = 9

    def get(self, request, *args, **kwargs):
        province_slug = self.kwargs.get("province_slug")
        sort_by = self.request.GET.get("sort", "default")

        queryset = Course.objects.filter(province_slug=province_slug, available=True)

        if sort_by == "price_asc":
            queryset = queryset.order_by("price")
        elif sort_by == "price_desc":
            queryset = queryset.order_by("-price")
        elif sort_by == "name":
            queryset = queryset.order_by("title")
        else:
            queryset = queryset.order_by("id")

        for course in queryset:
            image = course.courseimage_set.first()
            course.image = image

        paginator = Paginator(queryset, self.default_page_size)
        page_number = request.GET.get("page")
        paginated_courses = paginator.get_page(page_number)
        breadcrumbs = [
            ("Coursebook", reverse("home")),
            (
                province_slug,
                reverse("course_category", kwargs={"province_slug": province_slug}),
            ),
        ]

        context = {
            "courses": paginated_courses,
            "breadcrumbs": breadcrumbs,
            'slug':province_slug,
        }
        return render(request, self.template_name, context)
