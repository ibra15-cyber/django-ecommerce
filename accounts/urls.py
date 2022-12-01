from django.urls import path
from .views import (
            login_page, 
            register_page,
            activate_email,
            cart,
            add_to_cart,
            remove_cart,
            remove_coupon,
            success,

            user_profile,
            edit_profile,
            
        )

urlpatterns = [
     path("login/", login_page, name='login'), ##/accounts/login or {% url 'login' %}
     path("register/", register_page, name='register'),
     path("activate/<email_token>", activate_email, name="activate_email"),
     path("cart/", cart, name="cart"),
     path("add-to-cart/<uid>/", add_to_cart, name="add_to_cart"),
     path("remove-cart/<cart_item_uid>/",  remove_cart, name="remove_cart"),
     path("remove-coupon/<cart_id>", remove_coupon, name = "remove_coupon"),
     path("success/", success, name="success"),
     path("profile/<username>", user_profile, name='profile'),
     path("profile/<username>/edit-profile/", edit_profile, name="edit_profile" )

]
