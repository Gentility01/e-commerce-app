from django import template
from core.models import Order


register  = template.Library()  #this is to register our template tag

@register.filter
def cart_item_count(user):
    if user.is_authenticated:  #checking if the user is authenticated if not there wount be any item showed in there cart
        qs = Order.objects.filter(user=user, ordered=False)  # filter the Order by the user and making sure that ordered is false bcus we dont want it to get the previous order
        if qs.exists():
            return qs[0].items.count()
    return 0  #if the user is not authenticated we ae returning 0
    