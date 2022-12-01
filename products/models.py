from re import S

from django.db import models

from django.utils.text import slugify
# Create your models here.
from base.models import BaseModel


class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="categories")
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name) #use category name as slugigy
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self) -> str : #instead of returning a bunch of char for uuuid show me just the name
        return self.category_name
    
class ColorVariant(BaseModel): #creating a class for diff colors; inherits our base and stores in a char field
    color_name = models.CharField(max_length=120)
    price = models.IntegerField(default=0)       #color and size will now affect final price; so we save the price += to the main price

    def __str__(self) -> str: #instead of showing me chars show me the color names
        return self.color_name

class SizeVariant(BaseModel):
    size_name = models.CharField(max_length=120)
    price = models.IntegerField(default=0)

    def __str__(self) -> str :
        return self.size_name

class DeliveryTo(BaseModel):
    country_name = models.CharField(max_length=120)
    price = models.IntegerField(default=0)

    def __str__(self) -> str :
        return self.country_name


class Product(BaseModel):
    product_name = models.CharField( max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.IntegerField()
    product_description = models.TextField()

    color_variant= models.ManyToManyField(ColorVariant, null=True) #procut now has a field to store color and size and they inherite the classes as stated
    size_variant = models.ManyToManyField(SizeVariant, null=True)

    #mine 
    deli_country_name  = models.ManyToManyField(DeliveryTo, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self) -> str :
        return self.product_name

    
    def get_product_price_by_size(self, size):
        # when we invoke this on any product
        # get the price of that product, then 
        # get size name and take it's price and had to the product price
        return self.price + SizeVariant.objects.get(size_name = size).price
    

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="product")





class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)

