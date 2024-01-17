from rest_framework import serializers
from django.contrib.auth.models import Group
from django.db import transaction

from rest_framework.exceptions import ValidationError


from .models.app_user import AppUser
from .models.instructor import Instructor
from .models.course import Course
from .models.course_image import CourseImage
from .models.cart import Cart
from .models.cart_item import CartItem
from .models.blog_post import BlogPost
from .models.blog_category import BlogCategory
from .models.purchased_course import PurchasedCourse
from .models.participant import Participant
from .models.order_history import OrderHistory

from .helpers import create_thumbnail


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = [
            "id",
            "company_name",
            "password",
            "email",
            "phone_number",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        group = self.get_group_name_from_url()
        user = AppUser.objects.create_user(
            username=validated_data.get("email", ""), **validated_data
        )
        user.groups.add(group)
        return user

    def get_group_name_from_url(self):
        url = self.context.get("request").path
        group_name = "customer" if "register-customer" in url else "company"

        return Group.objects.get(name=group_name)


class InstructorSerializer(serializers.ModelSerializer):
    app_user = serializers.CharField(required=False)
    photo = serializers.ImageField(required=False)
    photo_thumb = serializers.ImageField(required=False)
    photo_change = serializers.CharField(write_only=True, required=False, default=False)

    class Meta:
        model = Instructor
        fields = "__all__"

    def update(self, instance, validated_data):
        if not validated_data.get("photo_change"):
            if photo := validated_data.pop("photo", None):
                if instance.photo:
                    instance.photo.delete(save=False)
                    instance.photo_thumb.delete(save=False)

                converted_photo = create_thumbnail(
                    photo, (400, 350), 80, thumb_name="orginal"
                )
                thumb = create_thumbnail(photo, (200, 150), 80, thumb_name="thumb")
                instance.photo = converted_photo
                instance.photo_thumb = thumb
            else:
                if instance.photo:
                    instance.photo.delete(save=False)
                    instance.photo_thumb.delete(save=False)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def create(self, validated_data):
        validated_data.pop("photo_change", None)
        app_user_id = self.context.get("request").user.id
        app_user = AppUser.objects.get(id=app_user_id)
        photo = validated_data.pop("photo", None)
        if photo:
            converted_photo = create_thumbnail(
                photo, (400, 350), 80, thumb_name="orginal"
            )
            thumb = create_thumbnail(photo, (200, 150), 80, thumb_name="thumb")
        else:
            converted_photo = None
            thumb = None

        instructor = Instructor.objects.create(
            app_user=app_user,
            photo=converted_photo,
            photo_thumb=thumb,
            **validated_data,
        )
        return instructor


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = "__all__"


class BlogPostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    photo = serializers.ImageField(required=False)
    photo_thumb = serializers.ImageField(required=False)
    photo_change = serializers.CharField(write_only=True, required=False, default=False)
    categories = BlogCategorySerializer(many=True, read_only=True)
    categories_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = BlogPost
        fields = "__all__"

    def update(self, instance, validated_data):
        if not validated_data.get("photo_change"):
            if photo := validated_data.pop("photo", None):
                if instance.photo:
                    instance.photo.delete(save=False)
                    instance.photo_thumb.delete(save=False)

                converted_photo = create_thumbnail(
                    photo, (1440, 540), 80, thumb_name="orginal"
                )
                thumb = create_thumbnail(photo, (200, 150), 80, thumb_name="thumb")
                instance.photo = converted_photo
                instance.photo_thumb = thumb
            else:
                if instance.photo:
                    instance.photo.delete(save=False)
                    instance.photo_thumb.delete(save=False)

        categories_ids = validated_data.pop("categories_ids", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        instance.categories.set(categories_ids)

        return instance

    def create(self, validated_data):
        validated_data.pop("photo_change", None)
        user_id = self.context.get("request").user.id
        company_user = AppUser.objects.get(id=user_id)
        photo = validated_data.pop("photo", None)
        if photo:
            converted_photo = create_thumbnail(
                photo, (1440, 540), 80, thumb_name="orginal"
            )
            thumb = create_thumbnail(photo, (200, 150), 80, thumb_name="thumb")
        else:
            converted_photo = None
            thumb = None

        categories_ids = validated_data.pop("categories_ids", [])

        blog_post = BlogPost.objects.create(
            user=company_user,
            photo=converted_photo,
            photo_thumb=thumb,
            **validated_data,
        )

        blog_post.categories.set(categories_ids)
        return blog_post


class ImageSerializer(serializers.ModelSerializer):
    # image_url = serializers.SerializerMethodField()

    class Meta:
        model = CourseImage
        fields = "__all__"

    def get_image_url(self, obj):
        if obj.image and obj.image.url:
            return obj.image.url
            # return self.context['request'].build_absolute_uri(obj.image.url)
        # return None


class ActiveProvincesSerializer(serializers.Serializer):
    province_name = serializers.CharField(source="province_slug", read_only=True)


class CourseSerializer(serializers.ModelSerializer):
    # instructor = InstructorSerializer()
    images = ImageSerializer(many=True, read_only=True)
    # carousel_image = serializers.SerializerMethodField()
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True, use_url=False),
        write_only=True,
        required=False,
    )

    photo_change = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False, default=[]
    )

    # def get_carousel_image(self, instance):
    #     carousel_image = instance.courseimage_set.first()
    #     return ImageSerializer(carousel_image).data if carousel_image else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        carousel_image = instance.courseimage_set.first()
        data["carousel_image"] = (
            ImageSerializer(carousel_image).data if carousel_image else None
        )

        return data

    class Meta:
        model = Course
        fields = "__all__"

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                if validated_data.get("photo_change"):
                    thumb_delete = False
                    course_images = CourseImage.objects.filter(course=instance)
                    photo_change = validated_data.get("photo_change")

                    images_to_delete_urls = [
                        img.image.url
                        for img in course_images
                        if img.image.url not in photo_change
                    ]
                    images_to_delete_ids = [
                        img.id
                        for img in course_images
                        if img.image.url in images_to_delete_urls
                    ]
                    if course_images.exists():
                        first_image = course_images.first()
                        if (
                            "thumb" in first_image.image_thumb.name
                            and first_image.image.url not in photo_change
                        ):
                            thumb_delete = True
                            first_image.delete()

                    if thumb_delete:
                        for img in course_images:
                            if img.image.url in photo_change:
                                converted_image = create_thumbnail(
                                    img.image, (550, 605), 80, thumb_name="orginal"
                                )

                                thumb = create_thumbnail(
                                    img.image, (200, 150), 80, thumb_name="thumb"
                                )
                                medium_thumb = create_thumbnail(
                                    img.image, (400, 200), 80, thumb_name="medium_thumb"
                                )
                                img.image.delete()
                                img.image = converted_image
                                img.image_thumb = thumb
                                img.image_medium_thumb = medium_thumb
                                img.save()
                                break

                    CourseImage.objects.filter(id__in=images_to_delete_ids).delete()
                else:
                    course_images = CourseImage.objects.filter(course=instance).delete()

                if validated_data.get("uploaded_images"):
                    uploaded_images = validated_data.pop("uploaded_images", [])
                    images_to_save = []
                    for idx, image in enumerate(uploaded_images):
                        if idx == 0 and not validated_data.get("photo_change"):
                            converted_image = create_thumbnail(
                                image, (550, 605), 80, thumb_name="orginal"
                            )
                            thumb = create_thumbnail(
                                image, (200, 150), 80, thumb_name="thumb"
                            )
                            medium_thumb = create_thumbnail(
                                image, (400, 200), 80, thumb_name="medium_thumb"
                            )
                            images_to_save.append(
                                CourseImage(
                                    course=instance,
                                    image=converted_image,
                                    image_thumb=thumb,
                                    image_medium_thumb=medium_thumb,
                                )
                            )
                        else:
                            image = create_thumbnail(
                                image, (550, 605), 80, thumb_name="orginal"
                            )
                            images_to_save.append(
                                CourseImage(course=instance, image=image)
                            )
                    CourseImage.objects.bulk_create(images_to_save)

                for attr, value in validated_data.items():
                    setattr(instance, attr, value)

                instance.save()
        except PermissionError as e:
            print(f"Błąd PermissionError: {e}")
        except Exception as e:
            print(f"Inny błąd: {e}")

        return instance

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        validated_data.pop("photo_change", None)
        course = Course.objects.create(**validated_data)
        images_to_save = []
        for idx, image in enumerate(uploaded_images):
            if idx == 0:
                converted_image = create_thumbnail(
                    image, (550, 605), 80, thumb_name="orginal"
                )
                thumb = create_thumbnail(image, (200, 150), 80, thumb_name="thumb")
                medium_thumb = create_thumbnail(
                    image, (400, 200), 80, thumb_name="medium_thumb"
                )
                images_to_save.append(
                    CourseImage(
                        course=course,
                        image=converted_image,
                        image_thumb=thumb,
                        image_medium_thumb=medium_thumb,
                    )
                )
            else:
                image = create_thumbnail(image, (550, 605), 80, thumb_name="orginal")
                images_to_save.append(CourseImage(course=course, image=image))
        CourseImage.objects.bulk_create(images_to_save)
        return course


# cart


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "quantity",
            "course",
            # "course_id",
        ]

    def create(self, validate_data):
        request = self.context.get("request")
        course = validate_data.get("course")
        quantity = validate_data.get("quantity")

        user = request.user
        current_cart = Cart.objects.filter(user=user, is_completed=False).first()
        if not current_cart:
            current_cart = Cart.objects.create(user=user)

        existing_cart_item = CartItem.objects.filter(
            cart=current_cart, course=course
        ).first()

        if existing_cart_item:
            new_quantity = existing_cart_item.quantity + quantity
            if new_quantity <= course.seats:
                existing_cart_item.quantity = new_quantity
                existing_cart_item.save()
            else:
                raise serializers.ValidationError("Niedostępna ilość miejsc w kursie")
        else:
            if quantity <= course.seats:
                CartItem.objects.create(
                    cart=current_cart, course=course, quantity=quantity
                )
            else:
                raise serializers.ValidationError("Niedostępna ilość miejsc w kursie")

        # if existing_cart_item:
        #     existing_cart_item.quantity += quantity
        #     existing_cart_item.save()
        # else:
        #     CartItem.objects.create(cart=current_cart, course=course, quantity=quantity)

        return current_cart


class CartItemDetailSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    cartItemId = serializers.IntegerField(source="pk", read_only=True)
    instructor = InstructorSerializer(source="course.instructor", read_only=True)
    images = ImageSerializer(source="course.courseimage_set.first", read_only=True)

    class Meta:
        model = CartItem
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    items = CartItemDetailSerializer(many=True, source="cartitem_set", read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ("name", "surname", "email", "phone")


class PurchasedCourseSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)
    # course = CourseSerializer(read_only=True)

    class Meta:
        model = PurchasedCourse
        fields = ("course", "quantity", "participants")

    def create(self, validated_data):
        return PurchasedCourse.objects.create(**validated_data)


class OrderHistorySerializer(serializers.ModelSerializer):
    purchased_courses = PurchasedCourseSerializer(many=True)
    user = serializers.CharField(required=False)
    order_date = serializers.DateTimeField(required=False)

    class Meta:
        model = OrderHistory
        fields = "__all__"

    def create(self, validated_data):
        user = self.context.get("request").user
        purchased_courses_data = validated_data.pop("purchased_courses")
        order_history = OrderHistory.objects.create(user=user, **validated_data)

        for purchased_course_data in purchased_courses_data:
            course = purchased_course_data.get("course")
            quantity = purchased_course_data.get("quantity")

            purchased_course = PurchasedCourse.objects.create(
                course=course, quantity=quantity
            )

            if "participants" in purchased_course_data:
                participants_data = purchased_course_data.get("participants")
                for participant_data in participants_data:
                    Participant.objects.create(
                        purchased_course=purchased_course, **participant_data
                    )
            order_history.purchased_courses.add(purchased_course)

        return order_history
