"""djstripe_example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


from .views import checkout_redirect, create_checkout_session, checkout_session_success

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("admin/", admin.site.urls),
    path(
        "checkout/redirect/<str:session_id>",
        checkout_redirect,
        name="checkout_redirect",
    ),
    path("checkout/create/", create_checkout_session, name="create_checkout_session"),
    path(
        "checkout/success/", checkout_session_success, name="checkout_session_success"
    ),
    path("djstripe/", include("djstripe.urls", namespace="djstripe")),
]
