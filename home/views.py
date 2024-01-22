from django.shortcuts import redirect, render
from products.models import Product
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='accounts/login/')
def index(request):
    products = Product.objects.all()
    print(products[0].product_name)
    return render(request,'home/index.html',context={'Products':products})
def search(request):
    if request.user:
        if request.method == 'POST':
            try:
                pname = request.POST.get('search')
                products=Product.objects.filter(product_name__icontains=pname)
                return render(request,'home/index.html',context={'Products':products})
            except Exception as e:
                print(e)      
    return redirect('/')
