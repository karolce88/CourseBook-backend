from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..models import Course
from ..serializers import CourseSerializer
from ..serializers import ActiveProvincesSerializer

class ActiveCoursesListView(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        limit = self.request.query_params.get('limit', None)
        queryset = Course.objects.filter(available=True)
        queryset = queryset.order_by('-id')
        if limit:
            queryset = queryset[:int(limit)]
        return queryset

    def list(self, request, *args, **kwargs):
        courses = self.get_queryset()
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

class CoursesByProvinceSlugView(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        province_slug = self.kwargs.get('province_slug')
        limit = self.request.query_params.get('limit', None)
        queryset = Course.objects.filter(available=True, province_slug=province_slug)
        queryset = queryset.order_by('-id')
        if limit:
            queryset = queryset[:int(limit)]
        return queryset

    def list(self, request, *args, **kwargs):
        courses = self.get_queryset()
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

class ActiveProvincesListView(generics.ListAPIView):
    serializer_class = ActiveProvincesSerializer

    def list(self, request, *args, **kwargs):
        provinces = Course.objects.filter(available=True).values('province_slug').distinct()
        serializer = self.get_serializer(provinces, many=True)
        return Response(serializer.data)