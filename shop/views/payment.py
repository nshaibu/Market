from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Order, ItemCategory


class PaymentView(LoginRequiredMixin, View):
    template_name = 'shop/payment.html'

    def get(self, request, *args, **kwargs):
        user_order = Order.get_user_pending_order(user=request.user)

        if user_order:
            context = {
                "categories": ItemCategory.objects.all(),
                'user_order': user_order,
            }
            return render(request, self.template_name, context=context)
        else:
            messages.warning(request, "Sorry you have no pending cart.")
        return redirect('shop:products')

    def post(self, request, *args, **kwargs):
        pass
