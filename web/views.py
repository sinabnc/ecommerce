from django.shortcuts import render,redirect
from .models import Product,Contact,Checkout
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from cart.cart import Cart
from django.core.paginator import Paginator
from django.contrib import messages
from django.conf import settings
import stripe

from django.views import View
# Create your views here.
def index(request):
   produ=Product.objects.all()
   paginator = Paginator(produ,3) 
   page_number = request.GET.get("page")
   page_obj = paginator.get_page(page_number)

   context={
    'page_obj':page_obj,
    'prod':produ
   }
   return render(request,"web/index.html",context)

def login1(request):
   if request.method=="POST":
        username=request.POST.get("name")
        password=request.POST.get('pass1')
        user = authenticate(request, username=username,password =password  )
       
        if user is not None:
            login(request,user)
            return redirect("index")
        else:
            messages.warning(request,'invalid details')
            return redirect("login")
   return render(request,'web/login.html')

def singup(request):
   if request.method=="POST":
      username=request.POST.get("name")
      firstname=request.POST.get("firstname")
      pass1=request.POST.get('pass1')
      pass2=request.POST.get('pass2')
      email=request.POST.get('email')

      if pass1!=pass2:
          messages.warning(request,"Enter same password")
      elif User.objects.filter(username=username).exists():
          messages.warning(request,'User already exist')

      else:
         if pass1==pass2:
            user = User.objects.create_user(username,email, pass1)
            user.first_name=firstname
            user.save()
            return redirect('login')
   return render(request,'web/singup.html')

def logout1(request):
    logout(request)
    return redirect("index")


@login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_detail(request):
    return render(request, 'web/cart.html')

def contact(request):
    if request.method=="POST":
        name=request.POST.get("fullname")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        text=request.POST.get("message")

        contact1=Contact(
            name=name,
            email=email,
            number=phone,
            text=text
        )
        contact1.save()

    return render(request,"web/contact.html")

def checkout(request):
    if request.method=="POST":
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        address=request.POST.get("address")
        house=request.POST.get("house")
        pin=request.POST.get("pin")

        check=Checkout(
             name=fname,
            email=email,
            number=phone,
            address=address,
            house=house,
            pin=pin

        )
        check.save()

    return render(request,'web/checkout.html')


def detail(request,slug):
    produ=Product.objects.filter(slug=slug)
    context={
        'prod':produ
    }
    return render(request,'web/detail.html',context)







stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def post(self, request, *args, **kwargs):
        price1 =Product.objects.all()
        

        for p in price1:
            price2 = p.price
            name1 = p.name



        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "inr",
                        "unit_amount": int(price2) * 100,
                        "product_data": {
                            "name": name1,
                           
                            
                        },
                    },
                    "quantity": 1,
                }
            ],
          
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        return redirect(checkout_session.url)