from django.urls import path
from .views import PayPalCreateOrderView, PayPalCaptureView, PayPalWebhookView

app_name = "payments"

urlpatterns = [
    path("paypal/create-order/<int:course_id>/", PayPalCreateOrderView.as_view(), name="paypal-create-order"),
    path("paypal/capture/", PayPalCaptureView.as_view(), name="paypal-capture"),
    path("paypal/webhook/", PayPalWebhookView.as_view(), name="paypal-webhook"),
]
