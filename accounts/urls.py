
from django.urls import path
from accounts.views import login_page,register,activate_email,logout_page,cart,remove_cart,remove_coupon,paymentSuccess
from products.views import add_to_cart,update_quantity
urlpatterns = [
    path('login/', login_page,name='login'),
    path('register/', register,name='register'),
     path('logout/',logout_page,name='logout'),
    path('activate/<email_token>/', activate_email,name='activate_email'),
    path('add-to-cart/<uid>/', add_to_cart,name='add_to_cart'),
    path('cart/',cart,name='cart'),
    path('remove-item/<uid>/', remove_cart,name='remove_cart_item'),
    path('update_quantity/',update_quantity,name='update_quantity'),
    path('remove-coupon/<cart_uid>/', remove_coupon,name='remove_coupon'),
    path('success/',paymentSuccess,name='success'),
]
