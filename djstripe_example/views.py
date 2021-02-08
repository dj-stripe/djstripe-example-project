import stripe
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView
from djstripe.enums import APIKeyType
from djstripe.models import APIKey, Price, Product

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def get_or_create_starter_price():
    try:
        product = Product.objects.get(metadata__djstripe_example="example_subscription")
    except Product.DoesNotExist:
        print("Could not find a subscription product to use. Will create one for you.")
        stripe_product = stripe.Product.create(
            name="Starter", metadata={"djstripe_example": "example_subscription"}
        )
        product = Product.sync_from_stripe_data(stripe_product)

    try:
        return Price.objects.get(metadata__djstripe_example="starter_price")
    except Price.DoesNotExist:
        print("Could not find a subscription price to use. Will create one for you.")
        stripe_price = stripe.Price.create(
            currency="usd",
            unit_amount="1200",
            recurring={"interval": "month"},
            product=product.id,
            metadata={"djstripe_example": "starter_price"},
        )
        return Price.sync_from_stripe_data(stripe_price)


class CheckoutRedirectView(TemplateView):
    template_name = "checkout_redirect.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        public_keys = APIKey.objects.filter(type=APIKeyType.publishable)[:1]
        if not public_keys.exists():
            url = self.request.build_absolute_uri("/admin/djstripe/apikey/add/")
            raise ImproperlyConfigured(
                "You must first configure a public key. "
                + f"Go to {url} to input your public key."
            )

        ctx["stripe_public_key"] = public_keys.get().secret
        ctx["checkout_session_id"] = self.kwargs["session_id"]

        return ctx


checkout_redirect = CheckoutRedirectView.as_view()


class CreateCheckoutSession(RedirectView):
    """
    A view to create a new Checkout session

    Similar to this tutorial:
    https://stripe.com/docs/billing/subscriptions/checkout

    We create the session, then redirect to the CheckoutRedirectView.
    """

    def get_redirect_url(self, *args, **kwargs):
        price = get_or_create_starter_price()

        checkout_session = stripe.checkout.Session.create(
            success_url="http://localhost:8000/checkout/success/?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8000/checkout/canceled/",
            mode="subscription",
            line_items=[{"price": price.id, "quantity": 1}],
            payment_method_types=["card"],
        )

        print(checkout_session)

        return reverse(
            "checkout_redirect", kwargs={"session_id": checkout_session["id"]}
        )


create_checkout_session = CreateCheckoutSession.as_view()
