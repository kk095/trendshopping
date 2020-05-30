from django.db import models
from django.db.models.signals import pre_save
from myapp.utils import unique_slug_generator
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class product(models.Model):
  product_id=models.AutoField
  slug=models.SlugField(max_length=250, blank=True)
  product_name=models.CharField(max_length=50)
  category=models.CharField(max_length=50,default="")
  sub_category=models.CharField(max_length=50,default="")
  desc=models.CharField(max_length=1000)
  price=models.IntegerField(default=0)
  discount_price=models.IntegerField(default=0,blank=True)
  new=models.BooleanField(default=False)
  pub_date=models.DateField()
  image=models.ImageField(upload_to='app/images',default="")
  image1 = models.ImageField(upload_to='app/images', default="")
  image2 = models.ImageField(upload_to='app/images', default="")
  image3 = models.ImageField(upload_to='app/images', default="")
  image4 = models.ImageField(upload_to='app/images', default="")

  def __str__(self):
    return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
      return self.name

def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
	    instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver, sender = product)


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    ordered = models.BooleanField(default=False)
    item=models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} of {self.item.product_name}"
    def total_price(self):
        return self.quantity * self.item.price
    def total_discountprice(self):
        return self.quantity * self.item.discount_price
    def final_price(self):
        if self.item.discount_price:
            return self.total_discountprice()
        else:
            return self.total_price()

class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    order_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)
    delivery_address=models.ForeignKey('CheckoutForm',on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.user.username
    def final(self):
        total=0
        for item in self.items.all():
            total += item.final_price()
        return total

class Promocode(models.Model):
           code= models.IntegerField(default=0)
           code_name=models.CharField(max_length=25,default="")
           def __str__(self):
               return self.code_name

class CheckoutForm(models.Model):
    user =models.CharField(max_length=20,default="")
    first_name= models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    phone=PhoneNumberField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zip=models.CharField(max_length=100)
    house_no=models.CharField(max_length=1000)
    address=models.CharField(max_length=1000)
    corresponding=models.CharField(max_length=1000)
    payment_mode=models.CharField(max_length=100,default="")
    def __str__(self):
        return self.first_name