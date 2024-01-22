from django.db import models
from base.emails import send_account_activation_email
from base.models import BaseModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from products.models import *
from django.contrib.auth import get_user_model


User=get_user_model()
# Create your models here.


class Profile(BaseModel):
    user= models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    is_email_verified=models.BooleanField(default=True)
    email_token=models.CharField(max_length=100,null=True,blank=True)
    profile_image= models.ImageField(upload_to='profile')

    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid=False,cart__user=self.user.profile).count()
    

#create post signal
    #instance is the newly created user
@receiver(post_save,sender = User)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance , email_token = email_token)
            email = instance.email
            send_account_activation_email(email , email_token)

    except Exception as e:
        print(e)

class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=50)
    is_expired=models.BooleanField(default=False)
    discount_price=models.IntegerField(default=100)
    min_amount=models.IntegerField(default=500)


class Cart(BaseModel):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='carts')
    coupon =models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    is_paid = models.BooleanField(default= False)
    razorpay_payment_id = models.CharField(max_length=100,null=True,blank=True)
    razorpay_order_id = models.CharField(max_length=100,null=True,blank=True)
    razorpay_signature = models.CharField(max_length=100,null=True,blank=True)
    def get_cost_total(self):
        price=[]
        for cart_item in self.cart_items.all():
            price.append((cart_item.product.price)*(cart_item.quantity))
            if cart_item.size_Variant:
                price.append(cart_item.size_Variant.price)
        print(price)
        return sum(price)
    def get_total(self):
        if self.coupon:
            if self.get_cost_total()>self.coupon.min_amount:
                return self.get_cost_total()-self.coupon.discount_price
            else:
                self.coupon=None
                self.save()
        return self.get_cost_total()
    

class CartItems(BaseModel):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')
    product = models.ForeignKey(Product,on_delete=models.SET_NULL ,null=True,blank=True,related_name='cart_product')
    size_Variant = models.ForeignKey(SizeVariant,on_delete=models.SET_NULL ,null=True,blank=True)
    quantity =  models.IntegerField(default=1)
    
    def get_product_price(self):
        price=[(self.product.price)*(self.quantity)]
        if self.size_Variant:
            price.append(self.size_Variant.price)
        return sum(price)

