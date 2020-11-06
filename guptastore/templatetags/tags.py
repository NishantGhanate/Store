from django import template
from django.template.defaultfilters import linebreaksbr, urlize
from api.models import Order , Category

register = template.Library()

@register.simple_tag
def number_of_items(request):
    if request.user.is_authenticated:
        try :
            customer = request.user.customer
            itemCountTag = Order.objects.get(customer=customer,checkout=False)
            return itemCountTag.get_cart_quantity
        except :
            return 0 
    else:
        return 0
    
@register.simple_tag
def get_categories(request):
    category = Category.objects.all()
    return  category

