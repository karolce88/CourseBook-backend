from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Course
import stripe
import json
from django.views.decorators.http import require_POST

stripe.api_key = settings.STRIPE_SECRET_KEY
WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_KEY


@require_POST
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers["Stripe-Signature"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        metadata = event["data"]["object"]["metadata"]
        course_info = metadata.get("course_info", [])

        for course_data in json.loads(course_info):
            course_id = course_data["course_id"]
            seats_purchased = course_data["seats_purchased"]

            course = Course.objects.get(id=course_id)
            course.seats -= seats_purchased
            course.save()

    return HttpResponse(status=200)
