from django.contrib import admin
from .models import Item, Order, OrderItem


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'price']
    list_editable = ['price']
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Item, ItemAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
