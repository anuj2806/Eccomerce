from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
# Create your models here.

class Categories(BaseModel):
    category_name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to='categorqies')
    slug= models.SlugField(unique=True,null=True,blank=True)

    def save(self,*args, **kwargs):
        self.slug=slugify(self.category_name)
        super(Categories,self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.category_name
    
class SizeVariant(BaseModel):
    product_size = models.CharField(max_length = 10)
    price= models.IntegerField(default=0)

    def __str__(self):
        return self.product_size

class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug= models.SlugField(unique=True,null=True,blank=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE,related_name='products')
    price= models.IntegerField()
    product_description=models.TextField()
    size_variant=models.ManyToManyField(SizeVariant,blank=True,related_name='size')

    def save(self,*args, **kwargs):
        self.slug=slugify(self.product_name)
        super(Product,self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name


class ProductImage(BaseModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_images')
    image = models.ImageField(upload_to='product')


    


#related name  is used to define the reverse relation from the related model back to the model
#    that defines the ForeignKey or OneToOneField
  