from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage

from .blog_category import BlogCategory
from .app_user import AppUser


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    short_content = models.TextField()
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    categories = models.ManyToManyField(BlogCategory, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def get_upload_path(instance, filename):
        company_name_slug = slugify(instance.user.company_name)
        post_title = slugify(instance.title)
        return f"blog/{company_name_slug}/{post_title}/{filename}"

    photo = models.ImageField(upload_to=get_upload_path, blank=True)
    photo_thumb = models.ImageField(upload_to=get_upload_path, blank=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

@receiver(pre_delete, sender=BlogPost)
def instructor_pre_delete(sender, instance, **kwargs):
    if instance.photo:
        default_storage.delete(instance.photo.path)
        default_storage.delete(instance.photo_thumb.path)
