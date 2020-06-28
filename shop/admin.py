from django.contrib import admin

from .models import *


# Register your models here.
admin.site.register([ItemCategory, Item, Coupon, Address, Order, OrderedItem])
