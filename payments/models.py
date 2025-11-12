from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models.student import Student
from courses.models.course import Course


class Payment(models.Model):
    class Status(models.TextChoices):
        CREATED = "created", "created"
        APPROVED = "approved", "approved"
        CAPTURED = "captured", "captured"
        FAILED = "failed", "failed"
        CANCELED = "canceled", "canceled"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="payments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default=getattr(settings, "DEFAULT_CURRENCY", "USD"))
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.CREATED)
    provider = models.CharField(max_length=20, default="paypal")
    provider_order_id = models.CharField(max_length=64, unique=True, blank=True, null=True)
    idempotency_key = models.CharField(max_length=64, unique=True, blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = []
        indexes = [
            models.Index(fields=["provider", "provider_order_id"]),
        ]

    def mark_captured(self):
        self.status = self.Status.CAPTURED
        self.paid_at = timezone.now()
        self.save(update_fields=["status", "paid_at"])
