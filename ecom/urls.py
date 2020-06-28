"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.views.generic import RedirectView

from users.views.reset_views import (UserPasswordChangeView,
                                     UserPasswordChangeDoneView,
                                     UserPasswordResetCompleteView,
                                     UserPasswordResetView,
                                     UserPasswordResetDoneView,
                                     UserPasswordResetConfirmView)


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    path('', RedirectView.as_view(url='/shop/')),

    path('accounts/', include('users.urls', namespace='users')),
    path('shop/', include('shop.urls', namespace="shop")),

    # Reset and Change
    path('password_change/', UserPasswordChangeView.as_view(), name="password_change"),
    path('password_change/done/', UserPasswordChangeDoneView.as_view(), name="password_change_done"),
    path('password_reset/', UserPasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/', UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

