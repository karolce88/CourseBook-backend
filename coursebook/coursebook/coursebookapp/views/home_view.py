from django.shortcuts import render
from rest_framework import generics
from rest_framework import serializers

from ..models.course import Course
from ..models.blog_post import BlogPost


class HomeView(generics.ListCreateAPIView):
    template_name = "pages/index.html"

    def get(self, request, *args, **kwargs):
        # recommended_courses = Course.objects.filter(instructor__isnull=False)
        recommended_courses = Course.objects.filter(available=True)
        posts = BlogPost.objects.all()[:4]

        for course in recommended_courses:
            image = course.courseimage_set.first()
            course.image = image

        context = {
            "recommended_courses": recommended_courses,
            "posts": posts,
        }
        return render(request, self.template_name, context)
