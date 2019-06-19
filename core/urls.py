from django.urls import path, include
from . import views


app_name = "core"

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('<slug>/product/', views.detail_product, name="product-detail"),
    path('<slug>/add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('<slug>/remove-from-cart/',
         views.remove_from_cart, name="remove-from-cart"),
    path('order-summary/', views.OrderSummary.as_view(), name="order-summary"),
    path('api/', include('core.api.urls'))
]
