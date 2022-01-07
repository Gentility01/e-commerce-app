from django.urls import path
from .views import (
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    CheckOutView,
    HomeView,
    PaymentView,
    ItemDetailView,
    OrderSummeryView,
    )

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home_view'),
    path('checkout', CheckOutView.as_view(), name='checkout'),
    path('order-summery/', OrderSummeryView.as_view(), name='summery-view'),
    path('detail/<slug>/', ItemDetailView.as_view(), name='detail-view'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),

]
#2:00:00