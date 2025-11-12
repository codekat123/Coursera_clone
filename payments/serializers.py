from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "student",
            "course",
            "amount",
            "currency",
            "status",
            "provider",
            "provider_order_id",
            "idempotency_key",
            "metadata",
            "created_at",
            "paid_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "provider",
            "provider_order_id",
            "created_at",
            "paid_at",
        ]
