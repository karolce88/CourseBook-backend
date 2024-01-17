from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from django.contrib import messages

from ..models.blog_post import BlogPost
from ..models.blog_category import BlogCategory

from ..serializers import BlogPostSerializer
from ..helpers import check_membership

from django.http import JsonResponse


@method_decorator(login_required(login_url="login"), name="dispatch")
class AccountBlogView(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = BlogPostSerializer
    template_name = "pages/account-blog.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        isMember = check_membership(user)
        posts = BlogPost.objects.filter(user=user)
        available_categories = BlogCategory.objects.all()

        context = {
            "user": user,
            "isMember": isMember,
            "posts": posts,
            "categories": available_categories,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            messages.success(request, "Wpis został utworzony")
            return JsonResponse({"message": "Wpis został utworzony"}, status=200)
        else:
            messages.error(request, "Nie udało się utworzyć wpisu. Spróbuj ponownie")
            errors = serializer.errors
            return JsonResponse(errors, status=400)
