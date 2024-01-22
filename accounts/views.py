from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from accounts.models import Profile,CartItems,Cart,Coupon
from products.models import Product
from django.contrib.auth import get_user_model
import razorpay
from django.conf import settings
from .utils import invoice_generated
User=get_user_model()
# Create your views here.


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)
        user_obj= User.objects.filter(username=email)
        print(user_obj)
        #1
        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)
        #2
        if not user_obj[0].profile.is_email_verified:
            print('ok')
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)
        #3
        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')

        

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)
    return render(request,'accounts/login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)
        user_obj= User.objects.filter(username=email)
        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.create(first_name=first_name,last_name=last_name,email=email,username=email)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)

    return render(request,'accounts/register.html')

def logout_page(request):
    logout(request)
    return redirect('/')

def activate_email(request,email_token):
    try:
        user=Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token')
    
def cart(request):
    cart = None
    cartItems = None
    payment=None
    try:
        cart = Cart.objects.get(is_paid=False,user__user=request.user)
        cartItems = CartItems.objects.filter(cart=cart)
    except Exception as e:
        print(e)
    
    if request.method=='POST':
        coupon = request.POST.get('coupon')
        print(coupon)
        if not Coupon.objects.filter(coupon_code = coupon):
            messages.warning(request, 'Invalid Coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if cart.coupon:
            messages.warning(request, 'Coupon already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if cart.get_cost_total() < Coupon.objects.get(coupon_code = coupon).min_amount:
            messages.warning(request, f'Amount must be greater than {Coupon.objects.get(coupon_code = coupon).min_amount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        cart.coupon=Coupon.objects.get(coupon_code = coupon)
        cart.save()
        messages.success(request, 'Coupon Applied')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    if cart:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        data = { "amount": cart.get_total()*100, "currency": "INR","payment_capture":1, "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        print(payment)
        cart.razorpay_order_id=payment['id']
        cart.save()
       
    return render(request,'accounts/cart.html',context={'Items':cartItems,'cart':cart,'payment':payment})
    
def remove_cart(request,uid):
    try:
        print(uid)
        cart_item  = CartItems.objects.get(uid=uid)
        print(cart_item)
        cart_item.delete()
    except Exception as e :
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_coupon(request,cart_uid):
    try:
        print(cart_uid)
        cart  = Cart.objects.get(uid=cart_uid)
        cart.coupon=None
        cart.save()
    except Exception as e :
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def paymentSuccess(request):
    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    razorpay_order_id = request.GET.get('razorpay_order_id')
    razorpay_signature = request.GET.get('razorpay_signature')
    cart = Cart.objects.get(razorpay_order_id=razorpay_order_id)
    if cart:
        cart.razorpay_payment_id=razorpay_payment_id
        cart.razorpay_signature=razorpay_signature
        cart.is_paid=True
        cart.save()
        customer_email = 'pratap00069@gmail.com' # Get the customer's email from your payment data
        amount = cart.get_total()  # Replace with the actual amount
        invoice_generated.send(sender=request, customer_email=customer_email, amount=amount)
        return redirect('/')
    return HttpResponse('Payment Successful')

