from django.db import models
from django.db.models.signals import post_save
import uuid
from products.models import (Product, ColorVariant, SizeVariant, Coupon)

# Create your models here.
from django.contrib.auth.models import User

from base.models import BaseModel
from base.email import send_account_activation_email
from django.dispatch import receiver


class Profile(BaseModel):
    user = models.OneToOneField(User,  on_delete=models.CASCADE, related_name="profile",)
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=120, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile')
    

    def get_cart_count(self):
        # cart_count = CartItems.objects.filter(cart__is_paid=False, cart__user = self.user).count()
        # print(cart_count)
        return CartItems.objects.filter(cart__is_paid = False, cart__user = self.user ).count()
       

@receiver(post_save, sender = User)
def send_email_token(sender, instance, created, **kwargs):
    try: 
        if created:
            email_token = str(uui.uuid4())
            Profile.objects.create(user = instance, email_token = email_token)
            email = instance.email
            send_account_activation_email(email, email_token)
    except Exception as e:
        print(e)


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    is_paid = models.BooleanField(default=False)

    # for our coupon 
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    # for razorpay 
    razor_pay_order_id = models.CharField(max_length=120, null=True, blank=True)
    razor_pay_payment_id = models.CharField(max_length=120, null=True, blank=True)
    razor_pay_payment_signature= models.CharField(max_length=120, null=True, blank=True)


    def get_cart_total_before_coupon(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.product.price)
            if cart_item.color_variant:
                color_variant_price = cart_item.color_variant.price
                prince.append(color_variant_price)
            if cart_item.size_variant:
                size_variant_price = cart_item.size_variant.price
                price.append(size_variant_price)


        # ########using coupon to subtract the price
        # if self.coupon: 
        #     print(self.coupon.minimum_amount)
        #     print(sum(price))
        #     if self.coupon.minimum_amount > sum(price):
        #         return sum(price) - self.coupon.discount_price #remove the discount from total cost
            
        return sum(price)


    #we totalling every thing in the cart
    #get all the items in cart 
    #for each check to see if it got extra charges, gether them together in a list called price and sum
    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.product.price)
            if cart_item.color_variant:
                color_variant_price = cart_item.color_variant.price
                prince.append(color_variant_price)
            if cart_item.size_variant:
                size_variant_price = cart_item.size_variant.price
                price.append(size_variant_price)


        ########using coupon to subtract the price
        if self.coupon: 
            print(self.coupon.minimum_amount)
            print(sum(price))
            if self.coupon.minimum_amount > sum(price):
                return sum(price) - self.coupon.discount_price #remove the discount from total cost
            
        return sum(price)

class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True )
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True  )


    #get the prices for a paricular item which includes: normal price + prices dues to color or size
    #into a list and sum them
    def get_product_price(self):
        price = [self.product.price]

        if self.color_variant:
            color_variant_price = self.color_variant.price
            price.append(color_variant_price)
        if self.size_variant: 
            size_variant_price = self.size_variant.price
            price.append(size_variant_price)
        return sum(price)

