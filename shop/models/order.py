from django.db import models

from users.models import User

from .item import Item
from .address import Address
from .coupon import Coupon


class OrderedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    ORDER_PENDING = "PENDING"
    ORDER_ORDERED = "ORDERED"
    ORDER_DELIVERED = "DELIVERED"
    ORDER_RECEIVED = "RECEIVED"
    ORDER_STATUS = (
        (ORDER_PENDING, "pending"),
        (ORDER_ORDERED, "ordered"),
        (ORDER_DELIVERED, 'deliver'),
        (ORDER_RECEIVED, 'received')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderedItem, related_name="order")
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address',
                                         on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(Address, related_name='billing_address',
                                        on_delete=models.SET_NULL, blank=True, null=True)
    # payment = models.ForeignKey(
    #     'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    order_status = models.CharField(choices=ORDER_STATUS, max_length=30)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_user_pending_order(cls, user=None):
        if user.is_authenticated:
            order_qs = cls.objects.filter(user=user, order_status=cls.ORDER_PENDING)
            return order_qs[0] if order_qs.exists() else None
        return None

    def get_sub_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

