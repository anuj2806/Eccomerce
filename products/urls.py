from django.urls import path
from products.views import get_product,add_to_cart

urlpatterns = [
    path('<slug>/', get_product,name='get_product'),
    
]