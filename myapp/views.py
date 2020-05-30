from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import Contact
from .models import product, OrderItem, Order, Promocode, CheckoutForm
from math import ceil
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from  django.utils import timezone
import random
from django.views.generic import View
import string
def Courses(request):
    x=order_summary(request)
    print(x)
    allprod=[]
    catprods=product.objects.values('category', 'id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        products=product.objects.filter(category=cat)
        n = len(products)
        nslides = (n // 4) + ceil((n / 4) - (n // 4))
        allprod.append([products,range(1,nslides),nslides])

    dct={'allprod':allprod,}
    return render(request,"index.html",dct)
def check(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.sub_category.lower( ):
        return True
    else:
        return False


def search(request):
    query=request.GET.get('search')
    allprod = []
    l=0
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(category=cat)
        prod=[item for item in prodtemp if check(query, item)]

        if len(prod)!=0:
            n = len(prod)
            l += n


            nslides = (n // 4) + ceil((n / 4) - (n // 4))
            allprod.append([prod, range(1, nslides), nslides])
    return render(request,'search.html', {'allprod':allprod, 'query':query,'l':l})



def handlesign(request):
    if request.method == 'POST':

        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        password=request.POST['password']
        repassword=request.POST['repassword']
        if len(username)>10:
            messages.warning(request, "WARNING! your username characters should not more than 10 characters")
            return redirect('home-page')
        if password!=repassword:
             messages.warning(request,"WARNING! your re-password is not matching.")
             return redirect('home-page')
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, " CONGRATULATION! your account has been successfully created")
        return redirect('home-page')
    else:
        return HttpResponse('not found')

def handlelog(request):
    if request.method=='POST':
        loginuser=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username=loginuser, password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"CONGRATULATION! logged in successfully.")
            return redirect('home-page')
        else:
            messages.warning(request,"INVALID CREDENTIALS! please try again.")
            return redirect('home-page')
    else:
        return HttpResponse('not found')

def handlelogout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request,"Successfully log out!")
        return redirect('home-page')
    else:
        return HttpResponse('not found')

def checkout(request, slug_field):
    prod = product.objects.filter(slug__iexact=slug_field)


    allprod = []
    catprods = prod.values('sub_category')
    products=product.objects.filter(sub_category__in=catprods)
    n = len(products)
    nslides = (n // 4) + ceil((n / 4) - (n // 4))
    allprod.append([products, range(1, nslides), nslides])

    dct = {'prod':prod[0],'allprod':allprod}
    return render(request, "checkout.html",dct)
def about(request):
    return render(request, "about.html")
def history(request):
    return render(request,"history.html")


@ login_required(login_url='/register/')
def order_summary(request):
    user=request.user
    #if user.is_authenticated:

    user_items= OrderItem.objects.filter(user=user,ordered=False)
    user_order=Order.objects.filter(user=user,ordered=False)
    items=user_items.values('quantity')
    count=0
    for x in items:
           count += x['quantity']

    context={'order':user_items,'count':count,'total':user_order

       }
    return render(request, 'order summary.html',context)
   # else:
    #    messages.info(request,"please register before checking Cart!")
     #   return redirect('register')

def register(request):
    return render (request,'register.html')





def contactus(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('mail', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('des', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        return redirect('home-page')
    return render(request,'contact us.html')

@ login_required(login_url='/register/')
def add_to_cart(request,slug):
    item=get_object_or_404(product,slug=slug)
    order_item,created=OrderItem.objects.get_or_create(item=item,user=request.user,ordered=False)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,"item quantity has been updated!")

        else:
            messages.info(request,"item has been added to your cart!")
            order.items.add(order_item)
    else:
        order_date=timezone.now()
        order=Order.objects.create(user=request.user, order_date=order_date)
        order.items.add(order_item)
        messages.info(request, "item has been added to your cart!")

    return redirect('home-page')

@ login_required(login_url='/register/')
def remove_from_card(request, slug):
    item = get_object_or_404(product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print(order_qs)
    if order_qs.exists():
        order = order_qs[0]
        print(order)
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            print(order_item)
            order.items.remove(order_item)
            OrderItem.delete(order_item)
            messages.info(request,"item has been remove to your cart!")
            return redirect(request.META['HTTP_REFERER'])


        else:
            messages.info(request,"this item is not  in your cart!")

            return redirect('home-page')

    else:
        messages.info(request, "you dont have active order!")

        return redirect('home-page')


def plus(request,slug):
    item=get_object_or_404(product,slug=slug)
    order_item,created=OrderItem.objects.get_or_create(item=item,user=request.user,ordered=False)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,"item quantity has been updated!")

        else:
            messages.info(request,"item has been added to your cart!")
            order.items.add(order_item)
    else:
        order_date=timezone.now()
        order=Order.objects.create(user=request.user, order_date=order_date)
        order.items.add(order_item)
        messages.info(request, "item has been added to your cart!")

    return redirect(request.META['HTTP_REFERER'])

def minus(request,slug):
    item = get_object_or_404(product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print(order_qs)
    if order_qs.exists():
        order = order_qs[0]
        print(order)
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            print(order_item)
            order_item.quantity -= 1
            order_item.save()
            messages.info(request,"item quantity has been minus!")
            return redirect(request.META['HTTP_REFERER'])


        else:
            messages.info(request,"this item is not  in your cart!")

            return redirect(request.META['HTTP_REFERER'])

    else:
        messages.info(request, "you dont have active order!")

        return redirect(request.META['HTTP_REFERER'])



def order_place(request):
    user_items= OrderItem.objects.filter(user=request.user,ordered=False)
    user_order=Order.objects.filter(user=request.user,ordered=False)
    item_length=user_order.values('items')
    items=user_items.values('quantity')
    count=0
    for x in items:
        count += x['quantity']
    promo=Promocode.objects.all()
    random_promo=random.choice(promo)
    promo_discount= -random_promo.code
    context={
        'count':count,
        'item':user_items,
        'order':user_order,
        'length':item_length,
        'promo':random_promo,
        'discount':promo_discount,
    }
    if request.method == "POST":
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        phone = request.POST.get('phone', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state','')
        zip = request.POST.get('zip','')
        homeaddress=request.POST.get('homeaddress','')
        address=request.POST.get('address','')
        correspondance=request.POST.get('corresponding-address','')
        payment=request.POST.get('paymentmode','')
        checkoutform=CheckoutForm(first_name=firstname,last_name=lastname,phone=phone,city=city,state=state,zip=zip,
                                  house_no=homeaddress,address=address,corresponding=correspondance,payment_mode=payment,
                                  user=request.user
                                  )
        checkoutform.save()
    return render(request,'order-place.html',context)





