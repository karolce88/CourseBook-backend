from django.db import models
from django.contrib.auth.models import User


class AppUser(User):
    company_name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def is_member(self, group_name):
        return self.groups.filter(name=group_name).exists()
