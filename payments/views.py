from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.conf import settings

from users.permissions import IsStudent
from courses.models.course import Course
from enrollments.models import Enrollment
from .models import Payment
from .paypal import create_order as paypal_create_order, capture_order as paypal_capture_order


class PayPalCreateOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, course_id):
        student = request.user
        course = get_object_or_404(Course, id=course_id)

        if Enrollment.objects.filter(student=student, course=course).exists():
            return Response({"detail": "Already enrolled in this course."}, status=status.HTTP_400_BAD_REQUEST)

        currency = request.data.get("currency") or getattr(settings, "DEFAULT_CURRENCY", "USD")

        # Create local payment record
        payment = Payment.objects.create(
            student=student,
            course=course,
            amount=course.price,
            currency=currency,
            status=Payment.Status.CREATED,
        )

        try:
            order = paypal_create_order(amount=str(course.price), currency=currency)
        except Exception as e:
            payment.status = Payment.Status.FAILED
            payment.save(update_fields=["status"]) 
            return Response({"detail": "Failed to create PayPal order.", "error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        payment.provider_order_id = getattr(order, "id", None)
        payment.save(update_fields=["provider_order_id"]) 

        approve_url = None
        for link in getattr(order, "links", []) or []:
            if getattr(link, "rel", "") == "approve":
                approve_url = getattr(link, "href", None)
                break

        return Response({
            "payment_id": str(payment.id),
            "order_id": payment.provider_order_id,
            "approve_url": approve_url,
        }, status=status.HTTP_201_CREATED)


class PayPalCaptureView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsStudent]

    @transaction.atomic
    def post(self, request):
        student = request.user
        order_id = request.data.get("order_id")
        if not order_id:
            return Response({"detail": "order_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        payment = get_object_or_404(Payment, provider_order_id=order_id, student=student)

        if payment.status == Payment.Status.CAPTURED:
            enrollment, _ = Enrollment.objects.get_or_create(student=student, course=payment.course)
            return Response({"detail": "Already captured", "enrollment_id": enrollment.id}, status=status.HTTP_200_OK)

        try:
            result = paypal_capture_order(order_id)
        except Exception as e:
            return Response({"detail": "Failed to capture PayPal order.", "error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        result_status = getattr(result, "status", "")
        if result_status != "COMPLETED":
            payment.status = Payment.Status.FAILED
            payment.save(update_fields=["status"]) 
            return Response({"detail": f"Unexpected capture status: {result_status}"}, status=status.HTTP_400_BAD_REQUEST)

        payment.mark_captured()
        enrollment, _ = Enrollment.objects.get_or_create(student=student, course=payment.course)

        return Response({
            "payment_id": str(payment.id),
            "status": payment.status,
            "enrollment_id": enrollment.id,
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name="dispatch")
class PayPalWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # TODO: Implement PayPal webhook signature verification using PAYPAL_WEBHOOK_ID
        # For now, acknowledge to avoid retries during local testing.
        return Response({"status": "received"}, status=status.HTTP_200_OK)
