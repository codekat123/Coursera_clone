import os
from django.conf import settings
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest


def _environment():
    env = getattr(settings, "PAYPAL_ENV", os.getenv("PAYPAL_ENV", "sandbox")).lower()
    client_id = os.getenv("PAYPAL_CLIENT_ID")
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET")
    if env == "live":
        return LiveEnvironment(client_id=client_id, client_secret=client_secret)
    return SandboxEnvironment(client_id=client_id, client_secret=client_secret)


def paypal_client():
    return PayPalHttpClient(_environment())


def create_order(amount: str, currency: str):
    client = paypal_client()
    request = OrdersCreateRequest()
    request.prefer("return=representation")
    request.request_body(
        {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": currency.upper(),
                        "value": str(amount),
                    }
                }
            ],
        }
    )
    response = client.execute(request)
    return response.result


def capture_order(order_id: str):
    client = paypal_client()
    request = OrdersCaptureRequest(order_id)
    request.request_body({})
    response = client.execute(request)
    return response.result
