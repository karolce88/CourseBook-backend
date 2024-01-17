from django.shortcuts import get_object_or_404
from ..models.app_user import AppUser


def check_membership(user):
    if user.is_authenticated:
        app_user = get_object_or_404(AppUser, id=user.id)
        return app_user.is_member(group_name="customer")
    return False
