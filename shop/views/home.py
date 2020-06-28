from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from ..models import ItemCategory, Order


class HomePage(View):
    template_name = 'shop/home.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context = {
            "categories": ItemCategory.objects.all(),
            'user_order': Order.get_user_pending_order(request.user),
        }
        return render(request, self.template_name, self.context)
