from django.contrib import admin
from .models.app_user import AppUser
from .models.instructor import Instructor
from .models.course import Course

from .models.course_image import CourseImage
from .models.cart import Cart
from .models.cart_item import CartItem

from .models.blog_category import BlogCategory
from .models.blog_post import BlogPost

#
from .models.purchased_course import PurchasedCourse
from .models.order_history import OrderHistory
from .models.participant import Participant


class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "instructor", "price", "seats", "date")


class AppUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "company_name", "first_name", "last_name")


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "course", "quantity")


admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Instructor)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseImage)
admin.site.register(Cart)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(BlogCategory)
admin.site.register(BlogPost)
admin.site.register(OrderHistory)
admin.site.register(Participant)
admin.site.register(PurchasedCourse)
