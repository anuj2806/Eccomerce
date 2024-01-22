from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Categories)

@admin.register(SizeVariant)
class SizeVariant(admin.ModelAdmin):
    list_display = ['product_size' , 'price']
    model = SizeVariant
# ProductImageAdmin is a class inheriting from admin.StackedInline.
# It defines the inline form for the ProductImage model within the Product model's admin.
class ProductImageAdmin(admin.StackedInline):
    model=ProductImage



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['product_name','price']
    inlines=[ProductImageAdmin]
