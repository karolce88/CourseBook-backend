from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..helpers import check_membership
from rest_framework import generics
from django.core.paginator import Paginator

from ..models import OrderHistory
from ..models import PurchasedCourse


@method_decorator(login_required(login_url="login"), name="dispatch")
class AccountView(generics.ListAPIView):
    template_name = "pages/account.html"
    default_pagination_size = 12

    def get(self, request, *args, **kwargs):
        user = request.user
        isMember = check_membership(user)

        # USER
        last_5_orders = OrderHistory.objects.order_by("-order_date")[:5]

        for order in last_5_orders:
            total_value = 0
            purchased_courses = order.purchased_courses.all()
            for purchased_course in purchased_courses:
                total_value += purchased_course.course.price * purchased_course.quantity

            order.total_value = total_value

        # COMPANY
        # sold_orders = get_last_8_purchased_courses_with_details(user)
        paginated_sold_orders = None   
        sold_orders = get_purchased_courses(user)
        if sold_orders:
            paginator = Paginator(sold_orders, self.default_pagination_size)
            page_number = request.GET.get("page")
            paginated_sold_orders = paginator.get_page(page_number)
            

        context = {
            "user": user,
            "isMember": isMember,
            "orders": last_5_orders,
            "sold_orders": paginated_sold_orders,
        }
        return render(request, self.template_name, context)

def get_purchased_courses(user):
    user_purchased_courses = PurchasedCourse.objects.filter(
        course__instructor__app_user=user
    ).order_by("-id")
    courses_with_details = []
    for purchased_course in user_purchased_courses:
        course = purchased_course.course
        instructor = course.instructor

        first_image = course.courseimage_set.first()
        image_url = first_image.image_thumb.url if first_image else None

        order = OrderHistory.objects.filter(purchased_courses=purchased_course).first()
        order_date = order.order_date if order else None

        courses_with_details.append(
            {
                "course_title": course.title,
                "course_description": course.course_description,
                "instructor_name": instructor.fullname,
                "course_image": image_url,
                "course_price": course.price,
                "quantity": purchased_course.quantity,
                'order_date': order_date,
            }
        )
    return courses_with_details


# def get_last_8_purchased_courses_with_details(user):
#     user_purchased_courses = PurchasedCourse.objects.filter(
#         course__instructor__app_user=user
#     ).order_by("-id")[:8]

#     courses_with_details = []
#     for purchased_course in user_purchased_courses:
#         course = purchased_course.course
#         instructor = course.instructor

#         first_image = course.courseimage_set.first()
#         image_url = first_image.image_thumb.url if first_image else None

#         courses_with_details.append(
#             {
#                 "course_title": course.title,
#                 "course_description": course.course_description,
#                 "instructor_name": instructor.fullname,
#                 "course_image": image_url,
#                 "course_price": course.price,
#                 "quantity": purchased_course.quantity,
#             }
#         )

#     return courses_with_details
