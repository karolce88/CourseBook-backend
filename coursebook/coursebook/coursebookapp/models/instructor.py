from django.db import models
from .app_user import AppUser
from django.utils.text import slugify
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage


class Instructor(models.Model):
    app_user = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name="instructors_created"
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    description = models.TextField()

    def get_upload_path(instance, filename):
        company_name_slug = slugify(instance.app_user.company_name)
        return f"instructors/{company_name_slug}/{filename}"

    photo = models.ImageField(upload_to=get_upload_path, blank=True)
    photo_thumb = models.ImageField(upload_to=get_upload_path, blank=True)

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.fullname


@receiver(pre_delete, sender=Instructor)
def instructor_pre_delete(sender, instance, **kwargs):
    if instance.photo:
        default_storage.delete(instance.photo.path)
        default_storage.delete(instance.photo_thumb.path)
