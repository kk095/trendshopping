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
    STATUS=(
            ('Not order','Not order'),
            ('Out for delivery','Out for delivery'),
            ('delivered','delivered'),
            )
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=20,default="")
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now=True)
    order_date=models.DateTimeField()
    complete_date=models.DateTimeField(null=True, blank=True)
    ordered=models.BooleanField(default=False)
    status = models.CharField(max_length=100, default="not order",choices=STATUS)
    payment_price=models.FloatField(default=0)
    delivery_address=models.ForeignKey('CheckoutForm',on_delete=models.SET_NULL,blank=True,null=True)



    def __str__(self):
        return f"{self.user}-({self.status})"

    def final(self):
        total=0
        for item in self.items.all():
            total += item.final_price()
        return total
    amount=property(final)
    class Meta:
        ordering=["status"]

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
    corresponding=models.CharField(max_length=1000,blank=True)
    payment_mode=models.CharField(max_length=100,default="")
    def __str__(self):
        return self.first_name
    class Meta:
        verbose_name_plural="Addresses"


class Reply(models.Model):
    reply_sno = models.IntegerField(primary_key=True)
    comment_reply = models.TextField()
    user = models.CharField(max_length=20)
    on_comment = models.ForeignKey('Comments',on_delete=models.CASCADE)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL)
    disliked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="disliked")
    total_liked = models.IntegerField(default=0)
    total_disliked = models.IntegerField(default=0)
    reply_time = models.DateTimeField()
    def __str__(self):
        return f"{self.comment_reply}"


class Comments(models.Model):
    sno=models.IntegerField(primary_key=True)
    comment = models.TextField()
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    user = models.CharField(max_length=20)
    time = models.DateTimeField(null=True,blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL)
    total = models.IntegerField(default=0)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="dislikes")
    total_dislike = models.IntegerField(default=0)
    all_reply = models.ManyToManyField(Reply, related_name='reply')
    def __str__(self):
        return f"comment by {self.user}"

class Like(models.Model):
    comment=models.ForeignKey(Comments,on_delete=models.CASCADE)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    total_likes = models.IntegerField(default=0)
    def __str__(self):
        return f"liked on '{self.comment}'"

class Dislike(models.Model):
    dislike_comment=models.ForeignKey(Comments,on_delete=models.CASCADE)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    total_Dislikes = models.IntegerField(default=0)
    def __str__(self):
        return f"disliked on '{self.dislike_comment}'"
