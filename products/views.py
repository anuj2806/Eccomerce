from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from products.models import Product
from accounts.models import *


# Create your views here.

def get_product(request,slug):
    try:
        price= 0 
        product = Product.objects.get(slug=slug)
        print(product)
        price = product.price
        if request.GET.get:
            variant = request.GET.get('variant')
            if variant:
                price += product.size_variant.get(product_size=variant).price
                print(price)
            if variant is None :
                variant='M'
            quantity = request.GET.get('quantity')
            if quantity:
                quantity = quantity
            if quantity is None :
                quantity=1
       
        return render(request ,'product/product.html',context={'Product':product,'Variant':variant,'Price':price,'Quantity':quantity} )

    except Exception as e:
        print(e)

def add_to_cart(request,uid):
    try:

        variant = request.GET.get('variant')
        quantity = request.GET.get('quantity')
        print(variant)
        product = Product.objects.get(uid=uid)
        print(product)
        user = request.user.profile
        print(user)
        #  Django provides a get_or_create method for models, which is a convenient way to retrieve an object if it exists or create it if it doesn't
        cart,created = Cart.objects.get_or_create(user=user,is_paid = False)
        print(user)
        cart_items = CartItems.objects.create(cart=cart,product=product,)
        if variant:
            size_variant= SizeVariant.objects.get(product_size = variant)
            cart_items.size_Variant = size_variant
            cart_items.save()
        if quantity:
            cart_items.quantity = quantity
            cart_items.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    except Exception as e:
        print(e)

def update_quantity(request):
    if request.method == 'POST':
        try:
            item_id = request.POST.get('item_id')
            new_quantity=request.POST.get('new_quantity')
            cart_item = CartItems.objects.get(uid=item_id)
            cart_item.quantity = new_quantity
            cart_item.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except Exception as e:
            print(e)        

