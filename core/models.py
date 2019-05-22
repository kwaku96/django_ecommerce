from django.db import models
from django.urls import reverse
from django.conf import settings


class Item(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=60)
    image = models.ImageField(upload_to="item_image")
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    description = models.TextField()
    discount_price = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)

    CATEGORY = (
        ('fr', 'Fruits'),
        ('vg', 'Vegetables'),
        ('tu', 'Tubers'),
    )

    category = models.CharField(max_length=2, choices=CATEGORY)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:product-detail', kwargs={"slug": self.slug})

    def add_to_cart(self):
        return reverse('core:add-to-cart', kwargs={"slug": self.slug})

    def remove_from_cart(self):
        return reverse('core:remove-from-cart', kwargs={"slug": self.slug})


class OrderItem(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.item.title

    def get_total_price(self):
        return self.quantity * self.item.price

    def get_total_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        return self.get_total_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField()
    ref_code = models.CharField(max_length=20)
    start_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def get_full_price(self):
        total_price = 0

        for order_item in self.items.all():
            total_price += order_item.get_final_price()
        return total_price
