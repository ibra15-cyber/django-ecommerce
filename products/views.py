from django.shortcuts import render, get_object_or_404
from .models import Product, SizeVariant
# from django.http import HttpResponseRedirect
# from accounts.models import *
# from accounts.models import Profile

# # # Create your views here.
# def get_product(request, slug):
#    template_name = 'product/product.html'
#    try: 
#       # product = get_object_or_404(Product, slug=slug)
#       product = Product.objects.get(slug=slug)
      # print(dir(product))
      # print(product)
      # print(dir(product.product_images))
      # print(product.product_images.all)
      # print(product.size_variant.count)
      
      
      # print(dir(product.size_variant.count))
   #    context = { 'product' : product}
   #    # context['product'] = product
   #    if request.GET.get('size'):
   #       size = request.GET.get('size')
   #       print(size)
   #       price = product.get_product_price_by_size(size)
   #       print(price)
   #       context['selected_size'] = size #passing size as value to a key called selected_size
   #       context['updated_price'] = price # same as above; so we are not only passing product but also these two
   #       print(context)
   #       # print("*" * 50)
   #       # print(price)
      
   #    return render(request, template_name, context=context)
   # except Exception as e:
   #    print(e)

def get_product(request, slug):
   print("*****************************")
   print(request.user.username)
   print(dir(request.user.username))
   print(request.user.profile.get_cart_count)
   print('******************************')

   product = get_object_or_404(Product, slug=slug)
   context = {'product': product}
   # print(dir(product))
   if request.GET.get('size'):
      size = request.GET.get('size')
      print(size)
      price = product.get_product_price_by_size(size)
      print(price)
      context['selected_size'] = size
      context['updated_price'] = price
      
   return render(request, 'product/product.html', context = context)

# product = Product.objects.get(slug = slug)
   #so lets talk about his
   #first it has got to do with getting a GET request after we select the radio selector
   #  <script > 
   #    function get_correct_price(size){
   #      console.log(size)
   #      window.location.href = window.location.pathname +  `?size=${size}`
   #    }
   #  </script>

# this script takes an arguement which is size and append a ?size=${size} to our url when we select any of the 
# radio buttons 



# onchange="get_correct_price('{{size.size_name}}')" 

# in our radio button we passed an onchanged to call our script 
# and in place of size it should get the our size we created here which in the views

# {% if selected_size == size.size_name %} checked {% endif %}

# we compare our selected_size and size.name if they are equal, check or select that particular radio button

   # def get_product_price_by_size(self, size):
   #      return self.price + SizeVariant.objects.get(size_name = size).price
   
   # this fn in model handles our price calculations
   # it takes the price we got on views adn return the initial price of that particular item 
   # and adds to it the variant price; by getting it using objects.get and equating size_name to size that comes 
   # through which we  will pass here as selected_size . its price


