from rest_framework.generics import RetrieveUpdateDestroyAPIView
from ..models.blog_post import BlogPost
from ..serializers import BlogPostSerializer

from django.contrib import messages
from django.http import JsonResponse


class BlogPostModify(RetrieveUpdateDestroyAPIView):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()


    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(self.request, "Wpis został zaktualizowany")
            return JsonResponse({"message": "Wpis został zaktualizowany"}, status=200)
        else:
            messages.error(
                self.request,
                "Nie udało się zaktualizować wpisu. Spróbuj ponownie",
            )
            errors = serializer.errors
            return JsonResponse(errors, status=400)
