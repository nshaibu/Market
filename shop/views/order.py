from django.shortcuts import render
from django.contrib import messages
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone

from ..models import Order, ItemCategory, OrderedItem


def get_user_cart(request):
    template_name = 'shop/cart.html'

    if request.method == 'GET':
        previous_url = request.META.get('HTTP_REFERER')

        user_order = Order.get_user_pending_order(request.user)
        if not user_order:
            messages.error(request, "You have no item in your cart.")
            return redirect(previous_url)

        context = {
            "categories": ItemCategory.objects.all(),
            'user_order': Order.get_user_pending_order(request.user),
        }
        return render(request, template_name, context)


# @login_required()
# def inc_dec_product_in_cart(request, ordered_item_id, op_type="increase"):
#     if request.method == "GET":
#         try:
#             item = OrderedItem.objects.get(id=ordered_item_id)
#         except OrderedItem.DoesNotExist:
#             return redirect('shop:home')


