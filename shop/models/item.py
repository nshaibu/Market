from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='media/images/items/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    total_in_stock = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    @property
    def unit_price(self):
        return self.price if self.discount_price is None else self.discount_price

    def get_product_pic_url(self):
        return None if not self.image else self.image.url

    def get_item_category(self):
        return self.category.all()[0]

    class Meta:
        ordering = ['-date_added']
