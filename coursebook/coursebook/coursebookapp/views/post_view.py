from django.shortcuts import render
from rest_framework import generics
from django.urls import reverse


from ..models.blog_post import BlogPost
from ..serializers import BlogPostSerializer


class PostDetailView(generics.RetrieveAPIView):
    serializer_class = BlogPostSerializer
    lookup_field = "slug"
    queryset = BlogPost.objects.all()
    template_name = "pages/post.html"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        breadcrumbs = [
            ("Coursebook", reverse("home")),
            ("Blog", reverse("blog")),
        ]
        

        if instance.categories.exists():
            first_category = instance.categories.first()
            breadcrumbs.append(
                (first_category.name, reverse("blog_category", kwargs={"slug": first_category.slug}))
            )

        breadcrumbs.append(
            (
                instance.title,
                reverse(
                    "post",
                    kwargs={
                        "slug": instance.slug,
                    },
                ),
            )
        )

        context = {
            "post": instance,
            "breadcrumbs": breadcrumbs,
        }

        return render(request, self.template_name, context)
