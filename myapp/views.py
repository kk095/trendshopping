from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Contact
from .models import product, OrderItem, Order, Promocode, CheckoutForm, Comments, Like, Dislike, Reply
from math import ceil
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import random
from django.conf  import settings
from django.views.generic import View
from datetime import datetime
from django.utils.crypto import get_random_string


def Courses(request):
    allprod=[]
    catprods = product.objects.values('category', 'id')
    if request.user.is_authenticated:
        user_items = OrderItem.objects.filter(user=request.user,ordered=False)
        items = user_items.values('quantity')
        count = 0
        for x in items:
                count += x['quantity']
    else:
        count = ""
    cats = {item['category'] for item in catprods}
    for cat in cats:
        products = product.objects.filter(category=cat)
        n = len(products)
        nslides = (n // 4) + ceil((n / 4) - (n // 4))
        allprod.append([products,range(1,nslides),nslides])
    dct={'allprod':allprod,'count':count}
    return render(request,"index.html",dct)

def check(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.sub_category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    if request.user.is_authenticated:
        user_items = OrderItem.objects.filter(user=request.user,ordered=False)
        items = user_items.values('quantity')
        count = 0
        for x in items:
            count += x['quantity']
    else:
        count = ''
    allprod = []
    l=0
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(category=cat)
        prod = [item for item in prodtemp if check(query, item)]
        if len(prod) != 0:
            n = len(prod)
            l += n
            nslides = (n // 4) + ceil((n / 4) - (n // 4))
            allprod.append([prod, range(1, nslides), nslides])
    return render(request,'search.html', {'allprod':allprod, 'query':query,'l':l,'count':count})


def handlesign(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        password = request.POST['password']
        repassword = request.POST['repassword']
        if len(username)>10:
            messages.warning(request, "WARNING! your username characters should not more than 10 characters")
            return redirect('home-page')
        if password != repassword:
             messages.warning(request,"WARNING! your re-password is not matching.")
             return redirect('home-page')
        user = authenticate(username=username, password=password)
        if user is not None:
            messages.info(request,"This username is already taken, choose unique!")
            return redirect('home-page')
        else:
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            login(request,myuser)
            subject = f"Thank you {username} for registering to Trend Shopping"
            message = f"HI! {fname} {lname}\n We are all really excited to welcome you to our team. At Trend Shopping, we care about giving our user everything they need to perform their best.Our team will help you setup your details and online accounts on your request.You can contact us any time whenever you need of us just click on the 'contact us' link and share your problems with us. Thanking You!"
            email_from = settings.EMAIL_HOST_USER
            email_to = [email]
            send_mail(subject, message, email_from, email_to,fail_silently=True,)
            messages.success(request, " CONGRATULATION! your account has been successfully created")
            return redirect('home-page')
    else:
        return HttpResponse('not found')


def handlelog(request):
    if request.method == 'POST':
        loginuser = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginuser, password=loginpassword)
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
    com = Comments.objects.filter(product=prod[0])
    for c in com:
        r=Reply.objects.filter(on_comment=c)
        for add in r:
            c.all_reply.add(add)
    ln=len(com)
    if request.user.is_authenticated:
        user_items= OrderItem.objects.filter(user=request.user,ordered=False)
        items=user_items.values('quantity')
        count=0
        for x in items:
            count += x['quantity']
    else:
        count=''
    allprod = []
    catprods = prod.values('sub_category')
    products=product.objects.filter(sub_category__in=catprods)
    n = len(products)
    nslides = (n // 4) + ceil((n / 4) - (n // 4))
    allprod.append([products, range(1, nslides), nslides])
    dct = {'prod':prod[0],'allprod':allprod,'com':com,'count':count,'ln':ln}
    return render(request, "checkout.html",dct)


def about(request):
    if request.user.is_authenticated:
        user_items= OrderItem.objects.filter(user=request.user,ordered=False)
        items=user_items.values('quantity')
        count=0
        for x in items:
            count += x['quantity']
    else:
        count=''
    return render(request, "about.html",{'count':count})


def history(request):
    if request.user.is_authenticated:
        user_items= OrderItem.objects.filter(user=request.user,ordered=False)
        items=user_items.values('quantity')
        count=0
        for x in items:
            count += x['quantity']
    else:
        count=''
    return render(request,"history.html",{'count':count})


@ login_required(login_url='/register/')
def order_summary(request):
    user_order=Order.objects.filter(user=request.user,ordered=False)
    if user_order.exists():
        user_items= OrderItem.objects.filter(user=request.user,ordered=False)
        items=user_items.values('quantity')
        count=0
        for x in items:
               count += x['quantity']
        context={'order':user_items,'count':count,'total':user_order}
        return render(request, 'order summary.html',context)
    return render(request,'order summary.html',{'count':0})


def register(request):
    if request.user.is_authenticated:
        user_items= OrderItem.objects.filter(user=request.user,ordered=False)
        items=user_items.values('quantity')
        count=0
        for x in items:
            count += x['quantity']
    else:
        count=''
    return render (request,'register.html',{'count':count})





def contactus(request):
    if request.user.is_authenticated:
        user_items= OrderItem.objects.filter(user=request.user,ordered=False)
        items=user_items.values('quantity')
        count=0
        for x in items:
            count += x['quantity']
    else:
        count=''
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('mail', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('des', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        subject=f"Thank you {name} for contact us"
        message= f"Thanks for reaching out. Satisfying our user is very important to us I hope we’ll stay in touch and get to work together again in the future. Please don’t hesitate to provide feedback and suggestions to help us improve, even from afar. We will contact you and reply to your text as soon as possible.Thanking You!"
        email_from= settings.EMAIL_HOST_USER
        email_to=[email]
        send_mail(subject, message, email_from, email_to,fail_silently=False,)
        subject='Try to contact'
        message= desc
        email_from= settings.EMAIL_HOST_USER
        email_to=['trendshoppingsite@gmail.com']
        send_mail(subject, message, email_from, email_to,fail_silently=False,)
        return redirect('home-page')
    return render(request,'contact us.html',{'count':count})

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
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
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
    user_items = OrderItem.objects.filter(user=request.user,ordered=False)
    user_order = Order.objects.filter(user=request.user,ordered=False)
    order = Order.objects.filter(user=request.user)
    item_length = user_order.values('items')
    items = user_items.values('quantity')
    count = 0
    for x in items:
        count += x['quantity']
    random_promo = 'null'
    promo_discount = 0
    if len(order) == 1:
        promo=Promocode.objects.filter(code=500)
        random_promo = promo[0]
        promo_discount +=  -promo[0].code
    elif len(order) != 1 and 15000 <= user_order[0].amount:
        promo = Promocode.objects.filter(code=250)
        random_promo=promo[0]
        promo_discount= -promo[0].code
    elif len(order) != 1 and 30000 <= user_order[0].amount:
        promo = Promocode.objects.filter(code=200)
        random_promo=promo[0]
        promo_discount= -promo[0].code
    elif len(order) != 1 and user_order[0].amount >= 50000:
        promo = Promocode.objects.filter(code=900)
        random_promo=promo[0]
        promo_discount= -promo[0].code


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
                                  user=request.user )
        checkoutform.save()
        if payment != 'Cash on Delivery':
            return redirect('payment')
        if payment == 'Cash on Delivery':
            return redirect('order-success')
    return render(request,'order-place.html',context)



class PaymentView(View):
    def get(self,*args, **kwargs):
        return render(self.request,'payment.html')


def order_success(request):
    usr=request.user
    order_check=Order.objects.get(user=request.user, ordered=False)
    check=Order.objects.filter(user=request.user, ordered=False)
    prod=OrderItem.objects.filter(user=request.user, ordered=False)
    item=prod
    ln= len(item)
    str=[i for i in item]
    s=""
    for i in range(ln):
        s+=(f"{str[i]}\n")
    price=check[0].amount
    alldelivery=CheckoutForm.objects.filter(user=request.user)
    delivery=alldelivery.last()
    x=datetime.now()
    random=get_random_string(length=15)
    user_items= OrderItem.objects.filter(user=request.user,ordered=False)
    for i in user_items:
        i.ordered=True
        i.save()
    subject='Order Confirmation Email'
    message= f"ORDER SUCCESSFUL!\n\nThank you very much {request.user} for your order!\n we have recieved your order.your order id is {random}.You will get your order very soon.We hope you enjoy our service.Please feel free to reach out if you have any query, suggestion, curiosities, problems,etc.You are always welcome to our 'Trend Shopping'.thanking you\n\n\n\n Order Id:\t{random}\t\t\t\t\t\t\tOrder Date:\t{datetime.now()}\n\nOrder Items :\n\n{s}\n\nOrder Amount:\t{price}\n\nAddress:\t{delivery.house_no} {delivery.address} {delivery.city} {delivery.state}"
    email_from= settings.EMAIL_HOST_USER
    email_to=[usr.email]
    send_mail(subject, message, email_from, email_to,fail_silently=False,)
    order_check.ordered=True
    order_check.unique_id=random
    order_check.payment_price= price
    order_check.delivery_address=delivery
    order_check.complete_date=x
    order_check.status='Out for delivery'
    order_check.save()
    nowtime=datetime.now()
    return render(request,'order-success.html',{'time':nowtime,'random':random})


def order_history(request):
    ord=Order.objects.filter(user=request.user,ordered=True,status='Out for delivery')
    user_items= OrderItem.objects.filter(user=request.user,ordered=False)
    items=user_items.values('quantity')
    count=0
    for x in items:
        count += x['quantity']
    order=ord.reverse()[::-1]
    print(order)
    context={'order':order,'count':count}
    return render(request,'order-history.html',context)

def comments(request,slug):
    if request.user.is_authenticated:
        pd = product.objects.filter(slug__iexact=slug)
        prod=pd[0]
        if request.method == 'POST':
                comment=request.POST.get('comment','')
                time=datetime.now()
                Comment = Comments(comment=comment, time=time, user=request.user, product=prod)
                Comment.save()
                return redirect(request.META['HTTP_REFERER'])
    else:
        messages.info(request,'Only after login, You can comment on product!')
        return redirect('register')


def like(request,my_int):
    if request.user.is_authenticated:
        cmt=Comments.objects.filter(sno=my_int)
        if Like.objects.filter(comment=cmt[0],user=request.user).exists():
            messages.success(request,'You have already like!')
            likes=Like.objects.filter(comment=cmt[0])
            total_likes=len(likes)
            return redirect(request.META['HTTP_REFERER'])
        else:
                likes=Like.objects.filter(comment=cmt[0])
                if not likes:
                    lik = Like(comment=cmt[0], total_likes=1)
                    lik.save()
                    print(cmt[0].total)
                    for x in cmt:
                        x.total=1
                        x.save()
                    lik.user.add(request.user)
                    cmt[0].likes.add(request.user)
                else:
                    likes[0].user.add(request.user)
                    cmt[0].likes.add(request.user)
                    l = likes[0].total_likes
                    lk=l+1
                    likes[0].total_likes = lk
                    likes[0].save()
                    for x in cmt:
                        x.total=lk
                        x.save()
                return redirect(request.META['HTTP_REFERER'])
    else:
        messages.info(request,'Only after login, you can like comments!')
        return redirect('register')




def dislike(request,my_int):
    if request.user.is_authenticated:
        cmt=Comments.objects.filter(sno=my_int)
        if Dislike.objects.filter(dislike_comment=cmt[0],user=request.user).exists():
            return redirect(request.META['HTTP_REFERER'])
        else:
            dislikes=Dislike.objects.filter(dislike_comment=cmt[0])
            if not dislikes:
                lik = Dislike(dislike_comment=cmt[0], total_Dislikes=1)
                lik.save()
                for x in cmt:
                    x.total_dislike=1
                    x.save()
                lik.user.add(request.user)
                cmt[0].dislikes.add(request.user)
            else:
                dislikes[0].user.add(request.user)
                cmt[0].dislikes.add(request.user)
                l = dislikes[0].total_Dislikes
                lk=l+1
                dislikes[0].total_Dislikes = lk
                dislikes[0].save()
                for y in cmt:
                    y.total_dislike = lk
                    y.save()
                return redirect(request.META['HTTP_REFERER'])
    else:
        messages.info(request,'Only after login, you can dislike comments!')
        return redirect('register')


def reply(request,sno):
    if request.user.is_authenticated:
        com = Comments.objects.filter(sno=sno)
        if request.method =='POST':
            rep = request.POST.get('reply','')
            comment=com[0]
            reply_time=datetime.now()
            new_reply=Reply(comment_reply=rep, user=request.user, on_comment=comment, reply_time=reply_time)
            new_reply.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        messages.warning(request,'only after login, you can reply!')
        return redirect('register')


