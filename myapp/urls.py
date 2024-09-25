from django.contrib import admin
from django.urls import path,include
from myapp import views

urlpatterns = [
    path('',views.Home,name="home"),
    path('registration/',views.registration,name="registration"),  
    path('login/',views.log_in,name="login"),
    path('logout/',views.log_out,name="logout"),
    path('forgot-password/',views.forgot_password,name="forgot_password"),
    path('confirm-password/',views.confirm_password,name="confirm_password"),
    path('checkout/',views.checkout,name="checkout"),
    path('product/',views.product,name="product"),
    path('store/',views.store,name="store"),  
    path('contact/',views.contact_me,name="contact"),  
    path('cart/<int:id>',views.cart,name="cart"),  
    path('carts/',views.cart_all_products,name="carts"),  
    path('add_to_wishlist/<int:id>',views.Add_to_Wishlist,name="addtowishlist"),  
    path('wishlist/',views.Wishlist,name="wishlist"),  
]
