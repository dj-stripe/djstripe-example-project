from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView
from djstripe.enums import APIKeyType
from djstripe.models import APIKey


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
