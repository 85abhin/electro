from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, HttpResponse, redirect
from .models import*
import random
from django.core.mail import send_mail
import razorpay

# Create your views here.
def Home(request):
    if 'email' in request.session: 
        uid = User.objects.get(email = request.session['email'])
        pid = Product.objects.all()
        cid = Cart.objects.all().filter(user = uid)

        con = {
            'products' : pid,
            'user' : uid,
            'cart' : cid.count,
            'cid': cid,
            
        }
        return render(request,'myapp/index.html',con)
    else:
        return render(request,'myapp/login.html')
    

def registration(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        uid = User.objects.create(name= name, email = email, password=password)
        uid.save()
        con ={
            'msg' : 'Registration Succesfully Done...'
        }
        return render(request,'myapp/registration.html',con)
    else:
        return render(request,'myapp/registration.html')
    
def log_in(request):
    if 'email' in request.session: 
        sid = User.objects.get(email = request.session['email'])
        return redirect('home')
    
    else:
        if request.POST:
            email = request.POST['email']
            password = request.POST['password']
            try:
                sid =User.objects.get(email= email)
                if email == sid.email:
                    if password == sid.password:
                        request.session['email'] = sid.email
                        return redirect('home')
                    else:
                        con ={
                            'message' : 'Invalid Password'
                        }
                        return render(request,'login.html',con)
                else:
                    con ={
                            'message' : 'Invalid email'
                        }
                    return render(request,'login.html',con)
            except:
                con ={
                            'message' : 'Invalid email and password'
                        }
                return render(request,'myapp/login.html',con)
        else: 
            return render(request,'myapp/login.html')

def log_out(request):
    if 'email' in request.session:
        del request.session['email']
        return render(request,'myapp/login.html')
    else:
        return render(request,'myapp/login.html')

def forgot_password(request):
    if request.POST:
        email = request.POST['email']
        otp = random.randint(1111,9999)
        sid = User.objects.get(email= email)
        sid.otp = otp
        sid.save()
        send_mail("Forgot Password","your OTP is "+str(otp),'gohiljayb10@gmail.com',[email])
        con = {
            'email': email
        }
        return render(request,'myapp/confirm-password.html',con)
    else:
        return render(request,'myapp/forgot_password.html')

def confirm_password(request):
    try:
        if request.POST:
            email = request.POST['email']
            OTP = request.POST['OTP']
            n_password = request.POST['n_password']
            c_password  = request.POST['c_password']
            uid = User.objects.get(email = email)

            if (email == uid.email) & (OTP == uid.otp) &  (n_password == c_password):
                uid.password == c_password
                uid.save()
                return render(request,'myapp/login.html',{'msg' :'password has changed successfully...'})
            else:
                if OTP != uid.otp:
                    return render(request,'myapp/confirm-password.html',{'msg':'Invalid Otp'})
                elif n_password != c_password:
                    return render(request,'myapp/confirm-password.html',{'msg':'Password does not match'})
                else:
                    return render(request,'myapp/confirm-password.html',{'msg':'Invalid OTP or Password doesnot match.. '})

        else:
            return render(request,'myapp/confirm-password.html')
    
    except:
        return render(request,'myapp/confirm-password.html')
    

def cart(request,id):
    if 'email' in request.session: 
        uid = User.objects.get(email = request.session['email'])
        pid = Product.objects.get(id = id)
        if Cart.objects.filter(user = uid, product = pid).exists():
            cid = Cart.objects.get(product = pid)
            cid.quantity = cid.quantity + 1 
            cid.total = cid.quantity * cid.product.o_price
            cid.save()
            return redirect('carts')
        else:
            cid = Cart.objects.create(user = uid,
                                    product = pid,
                                    quantity = pid.qty,
                                    total = pid.qty * pid.o_price)
            cid.save()
            return redirect('carts')
    else:
        return redirect('home')

def cart_all_products(request):
    if 'email' in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Cart.objects.all().filter(user = uid)
        Total = 0
        for c in cid:                                  # This is a for total the price and quantity in the cart.
            c.total = c.quantity * c.product.o_price
            c.save()
            Total+=c.total
        Total_amount = Total + 40
        client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))
        response = client.order.create({

                                        'amount': Total_amount,
                                        'currency':'INR',
                                        'payment_capture':1
            
        })
        con = {
            'products' : cid,
            'Total' : Total,
            'Total_Amount' : Total_amount,
            'cart' :cid.count,
            'response' :response,
        } 
        return render(request,'myapp/cart.html',con)


# this is a for adding product to wishlist...
def Add_to_Wishlist(request,id):
    if 'email' in request.session: 
        uid = User.objects.get(email = request.session['email'])
        pid = Product.objects.get(id = id)
        if WishList.objects.filter(user = uid, product = pid).exists():
            wid = WishList.objects.get(product = pid)
            wid.quantity = wid.quantity + 1 
            wid.total = wid.quantity * wid.product.o_price
            wid.save()
            return redirect('wishlist')
        else:
            wid = WishList.objects.create(user = uid,
                                    product = pid,
                                    quantity = pid.qty,
                                    total = pid.qty * pid.o_price)
            wid.save()
            return redirect('wishlist')
    else:
        return redirect('home')

def Wishlist(request):
    if 'email' in request.session:
        uid = User.objects.get(email = request.session['email'])
        wid = WishList.objects.all().filter(user = uid)
        Total = 0
        for c in wid:                                  # This is a for total the price and quantity in the cart.
            c.total = c.quantity * c.product.o_price
            c.save()
            Total+=c.total

        con = { 
            'wishlist' : wid,
        }
        return render(request,'myapp/wishlist.html',con)
    else:
        return render(request,'myapp/home.html')

def checkout(request):
    return render(request,'myapp/checkout.html')

def product(request):
    return render(request,'myapp/product.html')

def store(request):
    return render(request,'myapp/store.html')

def contact_me(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        sid = contact.objects.create(name = name, email = email, message = message)
        sid.save()
        return HttpResponse(contact) 
    else:
        return render(request,'myapp/contact.html')
