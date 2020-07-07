import random

from django.db import models
from django.db.models import Max

from .item import Item


class ItemCategory(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="media/images/categories/", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Item, related_name='category', blank=True)
    sub_category = models.ManyToManyField('self', related_name="parent_category", blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_random_category():
        max_id = ItemCategory.objects.all().aggregate(max_id=Max("id"))['max_id']
        while True:
            pk = random.randint(1, max_id)
            category = ItemCategory.objects.filter(pk=pk).first()
            if category:
                return category

    def get_category_pic_url(self):
        return None if not self.image else self.image.url
