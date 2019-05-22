from django.shortcuts import render, get_object_or_404, reverse, redirect
from .models import Item, Order, OrderItem
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(ListView):
    model = Item
    template_name = "item/home.html"
    paginate_by = 8


class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            redirect('/')
        context = {
            "object": order
        }
        return render(self.request, 'order_summary.html', context=context)


def detail_product(request, slug):
    item = get_object_or_404(Item, slug=slug)
    template = "item/product_detail.html"
    context = {"item": item}
    return render(request, template, context=context)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, ordered=False, user=request.user)

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            print('user has item in the list already\nincrease quantity')
            order_item.quantity += 1
            order_item.save()
        else:
            print('user does not have the items in list')
            order.items.add(order_item)
    else:
        print('this user has no order , time to create one')
        date_now = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=date_now)
        print('show a message that item has been added to cart')
        order.items.add(order_item)

    return redirect(reverse('core:product-detail', kwargs={"slug": slug}))


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        print('ok u have an order')
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug):
            order_item = OrderItem.objects.filter(
                user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            print('order has been removed')
    else:
        print('u dont have an order')

    return redirect(reverse('core:product-detail', kwargs={"slug": slug}))


@login_required
def remove_one_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            print('item is in your order')
            order_item = OrderItem.objects.filter(
                user=request.user, ordered=False)[0]

            if order_item.quantity > 1:
                print('u have more than one')
                order_item.quantity -= 1
                order_item.save()
            else:
                print('u have just one')
                order.items.remove(order_item)
                order_item.delete()
        else:
            print('item is not in your order')
    else:
        print(' you have no pending order to remove something from')

    return redirect(reverse('core:product-detail', kwargs={"slug": slug}))
