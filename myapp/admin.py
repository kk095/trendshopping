from django.contrib import admin

# Register your models here.
from .models import product
from .models import Contact
from .models import OrderItem
from .models import Order,Promocode,CheckoutForm

admin.site.register(product)
admin.site.register(Contact)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Promocode)
admin.site.register(CheckoutForm)
