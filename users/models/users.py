from django.db import models
from django.contrib.auth.models import AbstractUser

from django_countries.fields import CountryField


class User(AbstractUser):
    GENDER = (
        ('F', 'Female'),
        ('M', 'Male')
    )

    USER_TYPE_CUSTOMER = 'CUSTOMER'
    USER_TYPE_ADMIN = 'ADMIN'
    USER_TYPE = (
        (USER_TYPE_ADMIN, 'admin'),
        (USER_TYPE_CUSTOMER, 'customer')
    )

    user_type = models.CharField(choices=USER_TYPE, max_length=20)
    gender = models.CharField(choices=GENDER, max_length=10)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    street_address = models.CharField(max_length=80, null=True, blank=True)
    country = CountryField()
    city = models.CharField(max_length=80)
    region_or_state = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
