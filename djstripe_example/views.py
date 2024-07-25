import stripe
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView
from djstripe.enums import APIKeyType
from djstripe.models import APIKey, Price, Product, TaxRate

from django.views import View
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def get_or_create_starter_price():
    try:
        product = Product.objects.filter(
            metadata__djstripe_example="example_subscription"
        ).first()
    except Product.DoesNotExist:
        print("Could not find a subscription product to use. Will create one for you.")
        stripe_product = stripe.Product.create(
            name="Starter", metadata={"djstripe_example": "example_subscription"}
        )
        product = Product.sync_from_stripe_data(stripe_product)

    try:
        return Price.objects.filter(metadata__djstripe_example="starter_price").first()
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


def get_or_create_tax_rate():
    try:
        tax_rate = TaxRate.objects.get(metadata__djstripe_example="example_tax_rate")
    except TaxRate.DoesNotExist:
        print("Could not find a tax rate to use. Will create one for you.")
        stripe_tax_rate = stripe.TaxRate.create(
            display_name="VAT",
            description="VAT",
            inclusive=False,
            percentage=20,
            metadata={"djstripe_example": "example_tax_rate"},
        )
        tax_rate = TaxRate.sync_from_stripe_data(stripe_tax_rate)
    return tax_rate


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
        tax_rate = get_or_create_tax_rate()

        checkout_session = stripe.checkout.Session.create(
            success_url="http://localhost:8000/checkout/success/?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8000/checkout/canceled/",
            mode="subscription",
            line_items=[{"price": price.id, "quantity": 1, "tax_rates": [tax_rate.id]}],
            payment_method_types=["card"],
        )

        print(checkout_session)

        return reverse(
            "checkout_redirect", kwargs={"session_id": checkout_session["id"]}
        )


class CheckoutSessionSuccessView(View):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        if not session_id:
            return JsonResponse({"error": "No session ID provided."}, status=400)

        try:
            checkout_session = stripe.checkout.Session.retrieve(session_id)
            return JsonResponse(checkout_session, safe=False)
        except stripe.error.StripeError as e:
            return JsonResponse({"error": str(e)}, status=400)


create_checkout_session = CreateCheckoutSession.as_view()
checkout_session_success = CheckoutSessionSuccessView.as_view()
