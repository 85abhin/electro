from django.db import models
# Create your models here.

# This is contact me 
class contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message= models.TextField(max_length=500)

# This is a registration of user
class User(models.Model):
    name =models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    otp = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
  

# category choices
CATEGORY_CHOICES = (
 ('M', 'Mobile'),
 ('L', 'Laptop'),
 ('C', 'Cameras'),
 ('A', 'Accesories'),
)

# This is a model for all products..
class Product(models.Model):
    name = models.CharField(max_length=30)
    categories = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    price = models.IntegerField()
    o_price = models.IntegerField()
    offer = models.IntegerField()
    qty = models.PositiveIntegerField()
    pic = models.ImageField()
    dis = models.TextField()
    
    def __str__(self) -> str:
        return self.name
# add to cart 
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.IntegerField()

    # Below Property will be used by checkout.html page to show total cost in order summary
    # @property
    # def total_cost(self):
    #     return self.quantity * self.product.discounted_price

    # def __str__(self) -> str:
    #     return str(self.user_id)

# This is a address for the cart
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode=models.IntegerField()
    email = models.EmailField(max_length=100)
    address = models.TextField(max_length=200)
    phone_no =models.CharField(max_length=100)
    

class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.IntegerField()

    
