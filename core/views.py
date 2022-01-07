from django.contrib import messages
from django.core.checks.messages import Error
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http import request
from django.shortcuts import redirect, render, get_object_or_404
from .models import Item, OrderItem, Order, BillingAddress
from django.views.generic import DetailView, ListView, View
from .forms import CheckoutForm


from django.utils import timezone

# Create your views here.



class HomeView(ListView):
    model = Item
    template_name = 'index.html'
    paginate_by = 10
    
    
class OrderSummeryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object':order
            }
            return render(self.request, 'order_summery.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an activte order ')
            return redirect('/')
        
     
  
class CheckOutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form':form
        }
        return render(self.request, 'checkout.html', context)
    
    def post(self, *args, **kwargs): 
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                #TODO add functionality for these fields 
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                
                billing_address = BillingAddress(
                    user = request.self.user,
                    street_address = street_address,
                    appartment_address = apartment_address,
                    country = country,
                    zip = zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: add redirect to the selected payment option
                return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an activte order ')
            return redirect('core:checkout')
        
      
class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'payment.html')  #2:12:00
    
# def home_view(request):
#     context  = {
#         'items':Item.objects.all()
#     }
#     return render(request, 'index.html',context)


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'
    
@login_required
def add_to_cart(request, slug): #slug is the slug of the item
    item = get_object_or_404(Item,slug=slug)
    #checking if the user has an item or not 
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user = request.user,
        ordered = False  # odered=False will help ypu get an order that is not already purchased 
    )
    #checking if the user has an order and then modify the quantity in the order
    order_qs  = Order.objects.filter(user = request.user, ordered=False) #filter base on the user, ordered=false brings in oders that have not been completed
    
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order then adding it by incrementingn it
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1  #icrementint the cart here 
            order_item.save()
            messages.info(request, 'this item quantity was updated')
            return redirect('core:summery-view')
        else:
            messages.info(request, 'this item was added to your cart')
            order.items.add (order_item)
            return redirect('core:summery-view')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        
        order.items.add(order_item)
        messages.info(request, 'this item was added to your cart')
        return redirect('core:summery-view')

@login_required
def remove_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug) #getting the item 
    order_qs  = Order.objects.filter(user = request.user, ordered=False) # checking if the user has an order, filter base on the user, ordered=false brings in oders that have not been completed
    
    if order_qs.exists():
        order = order_qs[0]
        # filtering the order if the user has an order with the specific item slug 
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
            item=item,
            user = request.user,
            ordered = False  # odered=False will help ypu get an order that is not already purchased 
            )[0]
            order.items.remove (order_item)
            messages.info(request, 'this item was removed from your cart')
            return redirect('core:summery-view')
        else:
            # adding a message saying 
            messages.info(request, 'this item was not in your cart')
            return redirect('core:detail-view', slug=slug)  # this redirects you to the detailview with the specific slug     
    else:
        #adding a message saying that the user doesnt have an order
         messages.info(request, 'you do not have an active order')
         return redirect('core:detail-view', slug=slug)  # this redirects you to the detailview with the specific slug 1:20:40
        
    
    
@login_required
def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug) #getting the item 
    order_qs  = Order.objects.filter(user = request.user, ordered=False) # checking if the user has an order, filter base on the user, ordered=false brings in oders that have not been completed
    
    if order_qs.exists():
        order = order_qs[0]
        # filtering the order if the user has an order with the specific item slug 
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
            item=item,
            user = request.user,
            ordered = False  # odered=False will help ypu get an order that is not already purchased 
            )[0]
            if order_item.quantity >1:
                order_item.quantity -= 1  #decreasing the item by 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, 'this itemquantity was decreased')
            return redirect('core:summery-view')
        else:
            # adding a message saying 
            messages.info(request, 'this item was not in your cart')
            return redirect('core:detail-view', slug=slug)   # this redirects you to the detailview with the specific slug   
    else:
        #adding a message saying that the user doesnt have an order
         messages.info(request, 'you do not have an active order')
         return redirect('core:detail-view', slug=slug)   # this redirects you to the detailview with the specific slug 
        
        
    
    
    