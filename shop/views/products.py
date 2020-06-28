from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone

from ..models import ItemCategory, Item, OrderedItem, Order
from users.models import User


def get_category_detail(request, category_id):
    template_name = "shop/shop.html"

    if request.method == 'GET':
        page = request.GET.get("page", 1)

        try:
            category = ItemCategory.objects.get(id=category_id)
        except ItemCategory.DoesNotExist:
            return HttpResponseRedirect(reverse('shop:home'))

        products_paginator = Paginator(category.items.all(), 40)

        try:
            products_page = products_paginator.page(page)
        except PageNotAnInteger:
            products_page = products_paginator.page(1)
        except EmptyPage:
            products_page = products_paginator.page(products_paginator.num_pages)

        context = {
            "categories": ItemCategory.objects.all(),
            "category": category,
            "products": products_page,
            "user_order": Order.get_user_pending_order(request.user)
        }

        return render(request, template_name, context)


def get_product_details(request, product_id):
    template_name = "shop/product_detail.html"

    if request.method == "GET":
        ordered_item = None
        try:
            item = Item.objects.get(id=product_id)
        except Item.DoesNotExist:
            return HttpResponseRedirect(reverse('shop:home'))

        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            ordered_item, _ = OrderedItem.objects.get_or_create(user=user,
                                                                item=item, ordered=False)

        context = {
            "categories": ItemCategory.objects.all(),
            "product": item,
            "ordered_item": ordered_item,
            "user_order": Order.get_user_pending_order(request.user)
        }

        return render(request, template_name, context)


def add_remove_product_quantity(request, product_id, op_type="add"):
    if request.method == "GET":
        try:
            item = Item.objects.get(id=product_id)
        except Item.DoesNotExist:
            return HttpResponseRedirect(reverse('shop:home'))

        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            ordered_item_qs = OrderedItem.objects.filter(user=user,
                                                         item=item, ordered=False)

            if ordered_item_qs.exists():
                ordered_item = ordered_item_qs[0]
                if op_type == 'add':
                    if ordered_item.quantity < ordered_item.item.total_in_stock:
                        ordered_item.quantity += 1
                else:
                    if ordered_item.quantity != 0:
                        ordered_item.quantity -= 1
                ordered_item.save()
            else:
                OrderedItem.objects.create(user=user, item=item)
        else:
            messages.error(request, "Please you must sign up to place an order.")

        return HttpResponseRedirect(reverse('shop:product_detail', args=(product_id,)))


def add_to_cart(request, product_id):
    if request.method == "GET":
        try:
            item = Item.objects.get(id=product_id)
        except Item.DoesNotExist:
            return HttpResponseRedirect(reverse('shop:home'))

        if request.user.is_authenticated:

            ordered_item, _ = OrderedItem.objects.get_or_create(user=request.user,
                                                                item=item,
                                                                ordered=False)

            order_qs = Order.objects.filter(user=request.user, order_status=Order.ORDER_PENDING)
            if order_qs.exists():
                order = order_qs[0]

                if not order.items.filter(id=ordered_item.id).exists():
                    order.items.add(ordered_item)
            else:
                order = Order.objects.create(user=request.user,
                                             ordered_date=timezone.now(),
                                             order_status=Order.ORDER_PENDING)

                order.items.add(ordered_item)

            messages.info(request, "Item added to your cart.")
        else:
            messages.error(request, "Please you must sign up to place an order.")

        return HttpResponseRedirect(reverse("shop:product_detail", args=(product_id,)))


@login_required()
def increase_product_quantity_in_cart(request, ordered_item_id):

    if request.method == "GET":
        try:
            ordered_item = OrderedItem.objects.get(id=ordered_item_id)
        except OrderedItem.DoesNotExist:
            messages.error(request, "No such product in your cart")
        else:
            if ordered_item.quantity < ordered_item.item.total_in_stock:
                ordered_item.quantity += 1
                ordered_item.save()
                messages.success(request, "Quantity of product have been increased successfully.")
            else:
                messages.error(request, "Sorry you cannot order above %d items" % ordered_item.item.total_in_stock)

        return redirect('shop:user_cart')


@login_required()
def decrease_product_quantity_in_cart(request, ordered_item_id):

    if request.method == "GET":
        try:
            ordered_item = OrderedItem.objects.get(id=ordered_item_id)
        except OrderedItem.DoesNotExist:
            messages.error(request, "No such product in your cart")
        else:
            if ordered_item.quantity > 1:
                ordered_item.quantity -= 1
                ordered_item.save()
                messages.success(request, "Quantity of product have been decrease successfully.")
            else:
                messages.error(request, "Please the minimum you can order is one")

        return redirect('shop:user_cart')


@login_required()
def remove_item_from_cart(request, ordered_item_id):
    if request.method == "GET":
        try:
            ordered_item = OrderedItem.objects.get(id=ordered_item_id)
        except OrderedItem.DoesNotExist:
            messages.error(request, "No such product in your cart")
        else:
            if ordered_item.order.all().exists():
                order = ordered_item.order.all()[0]
                order.items.remove(ordered_item)

                ordered_item.delete()
                messages.success(request, "Product successfully removed from cart.")
            else:
                messages.error(request, "Sorry product not added to cart.")

        return redirect('shop:user_cart')
