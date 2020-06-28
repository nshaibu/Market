from django.shortcuts import render, redirect
from django.contrib import messages
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
# from django.utils import timezone

from ..models import Order, ItemCategory, OrderedItem, Address

from ..forms.checkout import CheckOutForm


def set_shipping_address_fields(form, shipping_address):
    form.fields['shipping_country'].initial = shipping_address.country
    form.fields['shipping_address'].initial = shipping_address.street_address
    form.fields['shipping_address2'].initial = shipping_address.apartment_address
    form.fields['shipping_region'].initial = shipping_address.region_or_state
    form.fields['shipping_zip'].initial = shipping_address.zip
    form.fields['shipping_user_email'].initial = shipping_address.email
    form.fields['shipping_user_phone_number'].initial = shipping_address.phone_number
    return form


def set_billing_address_fields(form, billing_address):
    form.fields['billing_country'].initial = billing_address.country
    form.fields['billing_address'].initial = billing_address.street_address
    form.fields['billing_address2'].initial = billing_address.apartment_address
    form.fields['billing_region'].initial = billing_address.region_or_state
    form.fields['billing_zip'].initial = billing_address.zip
    form.fields['billing_user_email'].initial = billing_address.email
    form.fields['billing_user_phone_number'].initial = billing_address.phone_number
    return form


@login_required()
def checkout(request):
    template_name = "shop/checkout.html"

    if request.method == "GET":
        shipping_address = billing_address = None
        form = CheckOutForm()

        user_pending_order = Order.get_user_pending_order(user=request.user)

        if user_pending_order is None:
            messages.warning(request, "Sorry you have no pending order")
            return redirect('shop:products')

        if user_pending_order.shipping_address and \
                user_pending_order.billing_address:
            form = set_billing_address_fields(form, user_pending_order.billing_address)
            form = set_shipping_address_fields(form, user_pending_order.shipping_address)
        else:
            shipping_address_qs = Address.objects.filter(user=request.user, default=True,
                                                         address_type=Address.SHIPPING_ADDRESS)
            if shipping_address_qs.exists():
                shipping_address = shipping_address_qs[0]
                form = set_shipping_address_fields(form, shipping_address)

            billing_address_qs = Address.objects.filter(user=request.user, default=True,
                                                        address_type=Address.BILLING_ADDRESS)
            if billing_address_qs.exists():
                billing_address = billing_address_qs[0]
                form = set_billing_address_fields(form, billing_address)

        context = {
            "categories": ItemCategory.objects.all(),
            'user_order': Order.get_user_pending_order(request.user),
            "form": form,
            "shipping_address": shipping_address,
            "billing_address": billing_address
        }

        return render(request, template_name, context=context)

    elif request.method == "POST":
        form = CheckOutForm(request.POST or None)

        if form.is_valid():
            user_pending_order = Order.get_user_pending_order(user=request.user)

            if user_pending_order is None:
                messages.warning(request, "Sorry you have no pending order")
                return redirect('shop:products')

            use_different_shipping_address = form.cleaned_data.get('use_different_shipping_address')

            billing_address_qs = Address.objects.filter(user=request.user,
                                                        address_type=Address.BILLING_ADDRESS,
                                                        country=form.cleaned_data.get('billing_country'),
                                                        street_address=form.cleaned_data.get('billing_address'),
                                                        apartment_address=form.cleaned_data.get('billing_address2'),
                                                        region_or_state=form.cleaned_data.get('billing_region'),
                                                        zip=form.cleaned_data.get('billing_zip'),
                                                        email=form.cleaned_data.get('billing_user_email'),
                                                        phone_number=form.cleaned_data.get('billing_user_phone_number'))
            if billing_address_qs.exists():
                billing_address = billing_address_qs[0]
            else:
                billing_address = Address.objects.create(user=request.user,
                                                         address_type=Address.BILLING_ADDRESS,
                                                         country=form.cleaned_data.get('billing_country'),
                                                         street_address=form.cleaned_data.get('billing_address'),
                                                         apartment_address=form.cleaned_data.get('billing_address2'),
                                                         region_or_state=form.cleaned_data.get('billing_region'),
                                                         zip=form.cleaned_data.get('billing_zip'),
                                                         email=form.cleaned_data.get('billing_user_email'),
                                                         phone_number=form.cleaned_data.get('billing_user_phone_number'))

            if not use_different_shipping_address:  # == 'off':
                shipping_address_qs = Address.objects.filter(user=request.user,
                                                             address_type=Address.SHIPPING_ADDRESS,
                                                             country=form.cleaned_data.get('shipping_country'),
                                                             street_address=form.cleaned_data.get('shipping_address'),
                                                             apartment_address=form.cleaned_data.get('shipping_address2'),
                                                             region_or_state=form.cleaned_data.get('shipping_region'),
                                                             zip=form.cleaned_data.get('shipping_zip'),
                                                             email=form.cleaned_data.get('shipping_user_email'),
                                                             phone_number=form.cleaned_data.get(
                                                                 'shipping_user_phone_number'))
                if shipping_address_qs.exists():
                    shipping_address = shipping_address_qs[0]
                else:
                    shipping_address = Address.objects.create(user=request.user,
                                                              address_type=Address.SHIPPING_ADDRESS,
                                                              country=form.cleaned_data.get('shipping_country'),
                                                              street_address=form.cleaned_data.get('shipping_address'),
                                                              apartment_address=form.cleaned_data.get('shipping_address2'),
                                                              region_or_state=form.cleaned_data.get('shipping_region'),
                                                              zip=form.cleaned_data.get('shipping_zip'),
                                                              email=form.cleaned_data.get('shipping_user_email'),
                                                              phone_number=form.cleaned_data.get(
                                                                  'shipping_user_phone_number'))
            else:
                shipping_address = billing_address

            user_pending_order.shipping_address = shipping_address
            user_pending_order.billing_address = billing_address
            user_pending_order.save()

        return redirect('shop:payment')
