from django.db import models
import uuid
#uuid is used to genrate unique identity for each products
class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at= models.DateField(auto_now=True)
    updated_at= models.DateField(auto_now_add=True)


#hera we use meta class abstract method so that we make django treat BaseModel as class 
# so that we inherit this class in other models to follow DRY
    class Meta:
        abstract = True