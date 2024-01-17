# Generated by Django 4.2.1 on 2023-08-13 07:36

import coursebookapp.models.course_image
import coursebookapp.models.instructor
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coursebookapp", "0005_course_province_slug_course_slug_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="courseimage",
            name="image_medium_thumb",
            field=models.ImageField(
                blank=True,
                upload_to=coursebookapp.models.course_image.CourseImage.get_upload_path,
            ),
        ),
        migrations.AddField(
            model_name="courseimage",
            name="image_thumb",
            field=models.ImageField(
                blank=True,
                upload_to=coursebookapp.models.course_image.CourseImage.get_upload_path,
            ),
        ),
        migrations.AddField(
            model_name="instructor",
            name="photo_thumb",
            field=models.ImageField(
                blank=True,
                upload_to=coursebookapp.models.instructor.Instructor.get_upload_path,
            ),
        ),
    ]