from django.shortcuts import render,redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm
from django.urls import reverse
from django.http import HttpResponse
from .forms import CustomerProfileForm
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib import messages
# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
    def get(self,request):
        topwears = Product.objects.filter(catagory='TW')
        bottomwears = Product.objects.filter(catagory='BW')
        mobiles = Product.objects.filter(catagory='M')
        laptop = Product.objects.filter(catagory='L')
        return render (request,'app/home.html',{'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'laptop':laptop})




# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html',{'product':product})



@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 print(product_id)
 product = Product.objects.get(id=product_id)
 Cart(user=user,product = product).save()
 return redirect("/cart")
#  else:
#     return redirect("/cart")


# def add_to_cart(request):
#     # Ensure the user is authenticated before proceeding
#     if not request.user.is_authenticated:
#         return HttpResponse("You must be logged in to add items to the cart.", status=401)

#     # Get the product_id from the request's GET parameters
#     product_id = request.GET.get('prod_id')

#     # Validate product_id
#     if not product_id:
#         return HttpResponse("Product ID is required.", status=400)

#     # Retrieve the corresponding product from the database or return a 404 response
#     product = get_object_or_404(Product, id=product_id)

#     # Create a new Cart instance associating the user and the product, and save it to the database
#     Cart.objects.create(user=request.user, product=product)

#     # Redirect the user to the "/cart" page
#     return redirect("/cart")

def show_cart(request):
   if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shiping_amount = 70
        total_amount = 0.0
        cart_product = [i for i in Cart.objects.all() if i.user==user]
        print(cart_product)
        if cart_product:
           for i in cart_product:
              
              tempamount = (i.quantity*(i.product.discounted_price))
              amount = amount+tempamount
              total_amount = amount+70  
              print(total_amount)
           return render(request,'app/addtocart.html',{'carts':cart,'total_amount':total_amount,
                                                    "amount":amount})
        else:
           return render(request,"app/emptycart.html")


#plus cart
def plus_cart(request):
   if request.method == "GET":
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity += 1
      c.save()
      amount = 0.0
      shiping_amount = 70
      total_amount = 0.0
      cart_product = [i for i in Cart.objects.all() if i.user==request.user]
      print(cart_product)
      if cart_product:
        for i in cart_product:
              
            tempamount = (i.quantity*(i.product.discounted_price))
            amount = amount+tempamount
            total_amount = amount+70  
            print(total_amount)
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'total_amount':total_amount
        }
        return JsonResponse(data)
      
# minus cart
def minus_cart(request):
   if request.method == "GET":
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity -= 1
      c.save()
      amount = 0.0
      shiping_amount = 70
      total_amount = 0.0
      cart_product = [i for i in Cart.objects.all() if i.user==request.user]
      print(cart_product)
      if cart_product:
        for i in cart_product:
              
            tempamount = (i.quantity*(i.product.discounted_price))
            amount = amount+tempamount
            total_amount = amount+70  
            print(total_amount)
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'total_amount':total_amount
        }
        return JsonResponse(data)

def remove_cart(request):
   if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shiping_amount = 70
        total_amount = 0.0
        cart_product = [i for i in Cart.objects.all() if i.user==request.user]
        for i in cart_product:              
            tempamount = (i.quantity*(i.product.discounted_price))
            amount = amount+tempamount
            total_amount = amount+70  
            print(total_amount)
        data = {
            'amount':amount,
            'total_amount':total_amount
        }
        return JsonResponse(data)



      
@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
 addr = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'addr':addr,'active':'btn btn-primary'})

@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{"order_placed":op})

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(catagory="M")
    elif data == 'redmi' or data=='samsung' or data == 'iphone':
        mobiles = Product.objects.filter(catagory="M").filter(brand=data)
    # elif data== 'below':
    #     mobiles = Product.objects.filter(catagory="M").filter(discounted_price_lt=10000)
    # elif da  ta== 'above':
    #     mobiles = Product.objects.filter(catagory="M").filter(discounted_price_gt=10000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})
 


# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation! Registered Succesfully')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})

def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shiping_amount = 70
 total_amount = 0.0
 cart_product = [i for i in Cart.objects.all() if i.user==request.user]
 print(cart_product)
 if cart_product:
    for i in cart_product:       
        tempamount = (i.quantity*(i.product.discounted_price))
        amount = amount+tempamount
        total_amount = amount+70  
        print(total_amount)
 return render(request, 'app/checkout.html',{'add':add,'totalamount':total_amount,'cart_items':cart_items})


def payment_done(request):
   user = request.user
   cust_id = request.GET.get('cust_id')
   customer = Customer.objects.get(id=cust_id)
   cart = Cart.objects.filter(user=user)
   for c in cart:
      OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
      c.delete()
   return redirect("orders")

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
   def get(self,request):
      form = CustomerProfileForm
      return render(request,'app/profile.html',{'form':form,'active':'btn btn-primary'})
   def post(self,request):
      form = CustomerProfileForm(request.POST)
      if form.is_valid():
         usr = request.user
         name = form.cleaned_data['name']
         locality = form.cleaned_data['locality']
         city = form.cleaned_data['city']
         state = form.cleaned_data['state']
         zipcode = form.cleaned_data['zipcode']
         reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
         reg.save()
         messages.success(request,'Congatulation your message has been updated in your profile succesfully')
      return render(request,'app/profile.html',{'form':form,'active':'btn btn-primary'})