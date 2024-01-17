from rest_framework.generics import RetrieveUpdateAPIView
from ..models import Course
from ..models.course_image import CourseImage
from ..serializers import CourseSerializer
from ..serializers import ImageSerializer
from django.http import JsonResponse
from django.contrib import messages


class EditCourseView(RetrieveUpdateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get(self, request, *args, **kwargs):
        course_pk = kwargs.get("pk", None)
        course = Course.objects.get(pk=course_pk)

        course_images = CourseImage.objects.filter(course=course)
        images_data = []

        for image in course_images:
            image_serializer = ImageSerializer(image, context={"request": request})
            images_data.append(image_serializer.data)

        serializer = self.serializer_class(course)
        serialized_data = serializer.data

        serialized_data["images"] = images_data

        return JsonResponse(serialized_data, status=200)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(self.request, "Kurs został zaktualizowany")
            return JsonResponse({"message": "Kurs został zaktualizowany"}, status=200)
        else:
            messages.error(
                self.request, "Nie udało się zaktualizować kursu. Spróbuj ponownie"
            )
            errors = serializer.errors
            return JsonResponse(errors, status=400)
