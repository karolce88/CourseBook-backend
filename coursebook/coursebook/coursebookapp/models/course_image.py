from typing import Iterable, Optional
from django.db import models
from django.utils.text import slugify
from .course import Course
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage


class CourseImage(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def get_upload_path(instance, filename):
        # course_slug = slugify(instance.course.title)
        return f"course_images/{instance.course.id}/{filename}"

    image = models.ImageField(upload_to=get_upload_path)
    image_thumb = models.ImageField(upload_to=get_upload_path, blank=True)
    image_medium_thumb = models.ImageField(upload_to=get_upload_path, blank=True)

    def __str__(self):
        return self.course.title


@receiver(pre_delete, sender=CourseImage)
def course_pre_delete(sender, instance, **kwargs):
    if instance.image:
        default_storage.delete(instance.image.path)
    if instance.image_thumb:
        default_storage.delete(instance.image_thumb.path)
        default_storage.delete(instance.image_medium_thumb.path)
