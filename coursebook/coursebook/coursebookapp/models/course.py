from django.db import models
from .instructor import Instructor
from django.utils.text import slugify


class Course(models.Model):
    instructor = models.ForeignKey(
        Instructor, on_delete=models.SET_NULL, null=True, blank=True
    )
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    province_choices = (
        ("dolnośląskie", "Dolnośląskie"),
        ("kujawsko-pomorskie", "Kujawsko-Pomorskie"),
        ("lubelskie", "Lubelskie"),
        ("lubuskie", "Lubuskie"),
        ("łódzkie", "Łódzkie"),
        ("małopolskie", "Małopolskie"),
        ("mazowieckie", "Mazowieckie"),
        ("opolskie", "Opolskie"),
        ("podkarpackie", "Podkarpackie"),
        ("podlaskie", "Podlaskie"),
        ("pomorskie", "Pomorskie"),
        ("śląskie", "Śląskie"),
        ("świętokrzyskie", "Świętokrzyskie"),
        ("warmińsko-mazurskie", "Warmińsko-Mazurskie"),
        ("wielkopolskie", "Wielkopolskie"),
        ("zachodniopomorskie", "Zachodniopomorskie"),
    )
    province = models.CharField(max_length=30, choices=province_choices)
    available = models.BooleanField(default=False)
    seats = models.PositiveIntegerField()
    date = models.DateField()
    time_start = models.TimeField()
    city = models.CharField(max_length=100)
    course_description = models.TextField()
    course_for = models.TextField()
    course_benefit = models.TextField()
    province_slug = models.SlugField(max_length=50, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.province_slug = slugify(self.province)
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
