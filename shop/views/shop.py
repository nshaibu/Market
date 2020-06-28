import random

from django.shortcuts import render, redirect
# from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import ItemCategory, Order


class ShopView(View):
    template_name = 'shop/shop.html'
    context = {
        "categories": ItemCategory.objects.all(),
    }

    def get(self, request, *args, **kwargs):
        category = ItemCategory.get_random_category()

        if category:
            page = request.GET.get("page", 1)

            products_paginator = Paginator(category.items.all(), 40)

            try:
                products_page = products_paginator.page(page)
            except PageNotAnInteger:
                products_page = products_paginator.page(1)
            except EmptyPage:
                products_page = products_paginator.page(products_paginator.num_pages)

            self.context['category'] = category
            self.context['products'] = products_page
            self.context['user_order'] = Order.get_user_pending_order(request.user)
        return render(request, self.template_name, self.context)


class ContactView(View):
    template_name = 'shop/contact.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context = {
            "categories": ItemCategory.objects.all(),
            'user_order': Order.get_user_pending_order(request.user),
        }
        return render(request, self.template_name, self.context)


class AboutView(View):
    template_name = 'shop/about.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context = {
            "categories": ItemCategory.objects.all(),
            'user_order': Order.get_user_pending_order(request.user),
        }
        return render(request, self.template_name, self.context)
