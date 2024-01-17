from django.shortcuts import render
from rest_framework import generics, permissions

from ..models import OrderHistory, PurchasedCourse, Participant
from django.db.models import Sum
from django.db.models import F, ExpressionWrapper, fields


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class OrderDetailsView(generics.RetrieveAPIView):
    queryset = OrderHistory.objects.all()
    template_name = "pages/order-details.html"
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        total_order_amount = (
            instance.purchased_courses.annotate(
                total_amount=ExpressionWrapper(
                    F("course__price") * F("quantity"),
                    output_field=fields.DecimalField(),
                )
            ).aggregate(total=Sum("total_amount"))["total"]
            or 0
        )

        purchased_courses_with_data = []
        for purchased_course in instance.purchased_courses.all():
            course = purchased_course.course
            first_image = course.courseimage_set.first()
            image_url = first_image.image_thumb.url if first_image else None
            participants = Participant.objects.filter(purchased_course=purchased_course)

            purchased_courses_with_data.append(
                {
                    "purchased_course": purchased_course,
                    "course_image": image_url,
                    "participants": participants,
                }
            )
        print(purchased_courses_with_data )
        context = {
            "order": instance,
            "purchased_courses": purchased_courses_with_data,
            "total_amount": total_order_amount,
        }

        return render(request, self.template_name, context)
