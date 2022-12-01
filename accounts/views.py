from cmath import log
from tkinter import E

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Profile, Cart, CartItems, Coupon
from products.models import * 
# import razarpay
from .forms import ProfileForm

#******************************************************************account login ************************************************************


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get("username")
        password = request.POST.get("password")

        user_obj = User.objects.filter(username = email)

        #if user account not found
        if not user_obj.exists():
            messages.warning(request, "Account not found")
            return HttpResponseRedirect(request.path_info)

        #if user account not verified
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, "Your account is not verified")
            return HttpResponseRedirect(request.path_info)
        
        #else if everything is okay
        user_obj = authenticate(username = email, password = password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')

        messages.success(request, "An email has been sent to your email account with a verification link")
        return HttpResponseRedirect(request.path_info)
    return render(request, "accounts/login.html")


#******************************************************************create account ************************************************************

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user_obj = User.objects.filter(username = email)
        print(user_obj)

        if user_obj.exists():
            messages.warning(request, "Email already taken")
            return HttpResponseRedirect(request.path_info)
        user_obj = User.objects.create(first_name = first_name, last_name = last_name, email = email, username=email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, "An email has been sent to your email account with a verification link")
        return HttpResponseRedirect(request.path_info)

    return render(request, "accounts/register.html")



#******************************************************************account activation  ************************************************************

def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token = email_token)
        user.is_email_verified = True 
        user.save()
        return redirect("/")
    except Exception as e:
        return HttpResponse("Invalid Email token")




#******************************************************************cart ************************************************************


def cart(request):
    # try: #using try except block there could be situations when is paid is yes; ie after payment
    cart_obj = Cart.objects.get(is_paid = False, user = request.user)
    # print((cart_obj.user)) #is_paid, get_cart_total, objects, user, user_id, uid
    # except Exception as e:
        # print(e)

    print(dir(cart_obj.cart_items))

    print("*******************************************")
    if request.method == "POST":        
        coupon = request.POST.get('coupon') #tapping from input field called coupon saving
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
        if not coupon_obj.exists(): #if the coupon entered by the user does not exit
            messages.warning(request, "Coupon is invalid!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if cart_obj.coupon: #if the coupon enetered already exist 
            messages.warning(request, "Coupon already exists!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart_obj.get_cart_total() > coupon_obj[0].minimum_amount:
            messages.warning(request, f"Amount should be greater than {coupon_obj[0].minimum_amount}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupon_obj[0].is_expired:
            messages.warning(request, f"Coupon has expired")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.success(request, "Coupon successfully applied!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    ###only process payment provided there is an item in cart
    # if cart_obj:
        # client = razarpay.Client(auth = (settings.KEY, settings.SECRET))
        # payment = client.order.create({'amount' : cart_obj.get_cart_total() * 100,  'currency': "INR", 'payment_capture': 1})
        # cart_obj.razor_pay_order_id = payment['id'] 
        # cart_obj.save()

    ##if no item in cart reset payment to None; i is_paid is True then set 
    # payment = None


    context = { 
        'cart' : cart_obj
       
    } #chenged from jsut cart_obj
    return render(request, 'accounts/cart.html', context)

#******************************************************************add to cart ************************************************************

# when we send a request with a variant attached ie when it got selected
# get the product by its id
# recognize the user making the request
# get a cart for the user and make paid field false
# create a cart item using the cart created above for the user and the product chose
# get the size variant attached to the item and pass the value to size_variant of the cart_itme
#save cart_item
#redirect to the same page
def add_to_cart(request, uid):
   variant = request.GET.get('variant')

   product = Product.objects.get(uid = uid)
   user = request.user
   cart , _ = Cart.objects.get_or_create(user = user, is_paid = False)
   
   cart_item = CartItems.objects.create(cart = cart, product = product)
   print(dir(cart_item.product))
   
   if variant:
      variant = request.GET.get('variant')
      size_variant = SizeVariant.objects.get(size_name = variant)
      cart_item.size_variant = size_variant
      cart_item.save()
      
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



#******************************************************************remove from cart ************************************************************


def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid = cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_coupon(request, cart_id): #the id here will be passed in the urls; 
    cart = Cart.objects.get(uid = cart_id) #get the cart for a particular user
    cart.coupon = None #turn the coupon off
    cart.save() 

    messages.success(request, "Coupon Removed.") #we call this metod after successful removing the coupon; will appear in the form where we called our alert file
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #this type of return does not need to render a template




#******************************************************************what to do after payment succeeds ************************************************************


# window.location.href = 'http://127.0.0.1:8000/accounts/success/?order_id=${response.order_id}
# from the above; when the processing of your payment goes through our url success = accounts/success above will get sent back to the user
# this request is a get request, so we say whenveer it gets that invokde success method 
# here.
# save the get requst with order id as order_id
# get all objects in cart with that order id
# set the paid status as true which will clear it from the cart becasue we set cart to display non paid items
# we save our cart for paid items 
# then say payment success
def success(request):
    order_id = request.GET.get('order_id')
    cart = Cart.objects.get(razor_pay_order_id = order_id)
    cart.is_paid = True
    cart.save()
    return HttpResponse("payment success")
    


def user_profile(request, username):
    user_obj = User.objects.get(username = username)
    # print("carts: ", user_obj)
    # print("date joined ", user_obj.date_joined)
    # print("id ", user_obj.id)
    # print("last login", user_obj.last_login)
    # # print("log enter", user_obj.logentry)
    # print("password", user_obj.password)
    # print("profile", user_obj.profile)

    return render(request, 'accounts/profile.html', context = {'user': user_obj})

def edit_profile(request, username):
    # we need to render the form fields first with initial values
    # before we use post request to change it
    user_obj = User.objects.get(username=username)
    context = {
        'user': user_obj
    }
    if request.method == 'POST':
        user_obj = User.objects.get(username=username)
        print(user_obj.email)
        email = request.POST.get("username")
        print(email)
        password = request.POST.get("password")
        context['email'] = email
        context['password'] = password
    # form = ProfileForm(POST or None, instance=user_obj)
        # if form.is_valid():
        #     form.save()
   

    return render(request, 'accounts/edit_profile.html', context=context)