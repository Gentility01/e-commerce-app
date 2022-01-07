from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
# Create your models here.


CATEGORY_CHOICES = (
    ('S','shirt') ,   # first entry goes into the database and thr second entry does into the template
    ('SW','Sport wear'),
    ('OW','Outwear'),
    ('SW','Sweater')
   
   
)

LABEL_CHOICES = (
    ('P','primary') ,   # first entry goes into the database and thr second entry does into the template
    ('S',' secondary'),
    ('D','danger')
   
)
class Item(models.Model):
    title   =  models.CharField( max_length=150)
    price   = models.FloatField()
    discount_price   = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)#2 is the number of the first entry 
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)    #1 is the number of the first entry 
    slug  = models.SlugField()
    description  = models.TextField()
    # quantity   = models.IntegerField(default=1)
    
    def __str__(self) :
        return self.title
    
    def get_absolute_url(self):
        return reverse("core:detail-view", kwargs={"slug": self.slug})
    
    def get_add_to_cart_url(self):
        return reverse("core:add_to_cart", kwargs={"slug":self.slug})
    
    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={"slug":self.slug})
    
    
    
    

class OrderItem(models.Model):
    user    =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered  = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity  = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} of  , {self.item.title}"
    
    def get_total_item_price(self):
        return self.quantity * self.item.price
    
    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_item_discount_price()
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()
    
    


class Order(models.Model):
    user    =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered  = models.BooleanField(default=False)
    items   = models.ManyToManyField(OrderItem)
    start_date  = models.DateTimeField( auto_now_add=True)
    ordered_date = models.DateTimeField()
    billing_address = models.ForeignKey('BillingAddress',on_delete=models.SET_NULL,blank=True, null=True)
    
    def __str__(self) :
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total +=order_item.get_final_price()
        return total
    
    
class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField( max_length=100)
    appartment_address = models.CharField( max_length=100)
    country  = CountryField(multiple=False)
    zip = models.CharField( max_length=100)
    
    def __str__(self):
        return self.user.username