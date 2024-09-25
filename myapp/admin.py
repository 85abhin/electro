from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(contact)
class AdminContact(admin.ModelAdmin):
    list_display = ['id','name','email','message']


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['id','name','email','password','otp']
 

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['id','name','categories','price','o_price','offer','qty','pic','dis']
 

@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ['user','product','quantity','total']
 
@admin.register(Address)
class AdminAddress(admin.ModelAdmin):
    list_display = ['first_name','last_name','country','city','pincode','email','address','phone_no']

@admin.register(WishList)
class AdminWishlist(admin.ModelAdmin):
    list_display = ['user','product','quantity','total']