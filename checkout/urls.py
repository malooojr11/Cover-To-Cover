from django.urls import path
from .views import stripe_transaction, paypal_transaction, stripe_config
from .webhooks import stripe_webhook
from paypal.standard.ipn.views import ipn

urlpatterns = [
    path('stripe/config', stripe_config, name='checkout.stripe.config'),
    path('stripe/webhook', stripe_webhook),
    path('stripe', stripe_transaction, name='checkout.stripe'),
    path('paypal', paypal_transaction, name='checkout.paypal'),
    path('paypal/webhook', ipn, name='checkout.paypal-webhook'),
]
