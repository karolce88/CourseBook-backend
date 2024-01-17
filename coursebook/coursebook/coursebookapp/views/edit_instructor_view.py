from rest_framework.generics import RetrieveUpdateAPIView
from ..models import Instructor
from ..serializers import InstructorSerializer

from django.contrib import messages
from django.http import JsonResponse


# sprawdzić komuniakty
class EditInstructorView(RetrieveUpdateAPIView):
    serializer_class = InstructorSerializer
    queryset = Instructor.objects.all()

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(self.request, "Prowadzący został zaktualizowany")
            return JsonResponse(
                {"message": "Prowadzący został zaktualizowany"}, status=200
            )
        else:
            messages.error(
                self.request,
                "Nie udało się zaktualizować prowadzącego. Spróbuj ponownie",
            )
            errors = serializer.errors
            return JsonResponse(errors, status=400)
