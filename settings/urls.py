from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from two_factor.urls import urlpatterns as tf_urls # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path("__reload__/", include("django_browser_reload.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("payments/", include("payments.urls")),
    path("2fa/", include(tf_urls, namespace="two_factor")),
    path("game/", include("content.urls")),
    path("", include("landing.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)