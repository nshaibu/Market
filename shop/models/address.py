from django.db import models
from django_countries.fields import CountryField

from users.models import User


class Address(models.Model):
    BILLING_ADDRESS = "BILLING"
    SHIPPING_ADDRESS = "SHIPPING"

    ADDRESS_CHOICES = (
        ('BILLING', 'Billing'),
        ('SHIPPING', 'Shipping'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    region_or_state = models.CharField(max_length=80, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    address_type = models.CharField(max_length=20, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name_plural = 'Addresses'
