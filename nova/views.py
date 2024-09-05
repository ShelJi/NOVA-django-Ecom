from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from nova.forms import *
from django.contrib import messages
from django.db import transaction

# class AddressRequiredMixin:
#     def isvalidaddress(self, request):
#         data = UserdataModel.objects.filter(datauser=request.user).first()
#         print("AddressRequiredMixin")
#         if data:
#             pass
#         else:
#             return redirect(reverse("profile"))

def redirecter(request, **kwargs):
    return redirect(reverse("home"))

def loginredirecter(request, **kwargs):
    return redirect(reverse("login"))

class IndexView(View):
    def get(self, request):
        lDeals = LatestDeals.objects.all()
        
        mobile= ProductData.objects.filter(category= "mobile") 
        headphone= ProductData.objects.filter(category= "headphone") 
        case= ProductData.objects.filter(category= "case") 
        watch= ProductData.objects.filter(category= "watch") 
        gadget= ProductData.objects.filter(category= "gadget") 
        laptop= ProductData.objects.filter(category= "laptop") 
        battery= ProductData.objects.filter(category= "battery") 
        electronics= ProductData.objects.filter(category= "electronics") 
        
        return render(request, "index.html", {"title": "",
                                              "mobiles": mobile,
                                              "headphones": headphone,
                                              "cases": case,
                                              "watchs": watch,
                                              "gadgets": gadget,
                                              "laptops": laptop,
                                              "batterys": battery,
                                              "electronics": electronics,
                                              "lDeals": lDeals})
    
class SignupView(View):
    def get(self, request):
        form = SignupModel()
        return render(request, "log.html", {"title": "Sign Up",
                                            "topic": "Sign Up",
                                            "form": form})
        
    def post(self, request):
        form = SignupModel(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect(reverse('login'))
        else:
            form = SignupModel()
            alert = "User Already Exists"
            
        return render(request, "log.html", {"title": "Sign Up",
                                            "topic": "Sign Up",
                                            "form": form,
                                            "alerts": alert})
            
class LoginView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "log.html", {"title": "Login",
                                            "topic": "LOGIN",
                                            "form": form})
    
    def post(self, request):
        alert = ""
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username= username, password= password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home'))
            else:
                alert = "Invalid user"
                messages.success(request, "Invalid user")
                
        return render(request, "log.html", {"title": "Login",
                                            "topic": "LOGIN",
                                            "alerts": alert,
                                            "form": form})

class LogoutView(LoginRequiredMixin, View):
    login_url = "/login/"
    
    def get(self,request):
        logout(request)
        return redirect(reverse('home'))
    
class ProfileView(LoginRequiredMixin, View):
    login_url= "/login/"
    
    def get(self, request, *args, **kwargs):
        
        datas = UserdataModel.objects.filter(datauser=request.user).first()
        
        return render(request, "profile.html", {"title": request.user,
                                                "data": datas})
        
    def post(self, request, *args, **kwargs):
        datas = UserdataModel.objects.filter(datauser=request.user).first()
        
        if datas:
            form = UserDataForm(request.POST, instance=datas)
        else:
            form = UserDataForm(request.POST)
            
        if form.is_valid():
            userform = form.save(commit=False)
            userform.datauser = request.user
            userform.profilestatus = True
            userform.save()
            return redirect(reverse('cartview'))
        else:
            alert = form.errors
        datas = UserdataModel.objects.filter(datauser=request.user).first()
        
        return render(request, "profile.html", {"title": request.user,
                                                "alerts": alert,
                                                "data": datas})
        
class ProductView(View):
    def get(self, request, *args, **kwargs):
        ptype = kwargs.get("ptype")
        pid = kwargs.get("pid")
        datas = ProductData.objects.filter(id= pid)
        return render(request, "product.html", {"title": ptype,
                                                "datas": datas})

class CategoryView(View):
    def get(self, request, *args, **kwargs):
        ptype = kwargs.get("ptype")
        datas = ProductData.objects.filter(category= ptype)
        return render(request, "category.html", {"title": ptype,
                                                 "datas": datas,
                                                 "category": ptype})
                
class CartView(LoginRequiredMixin, View):
    login_url = "/login/"
    
    def get(self, request, *args, **kwargs):
        cartDatas = CartModel.objects.filter(usercart =request.user)
        
        return render(request, "cart.html", {"title": "cart:)",
                                             "cartDatas": cartDatas,
                                             "cart": True})
    
    def post(self, request, *args, **kwargs):
        user = request.user
        pid = request.POST.get("pid")
        pid = int(pid)
        cnt = int(request.POST.get("cnt", 1))
            
        cart, create = CartModel.objects.get_or_create(usercart_id=user.id, productcart_id=pid)
        
        if create:
            cart.countval = 1
        else:
            cart.countval += cnt
            
        if request.POST.get("conscnt"):
            cart.countval = int(request.POST.get("conscnt"))
            
        if cart.countval > 10: 
            cart.countval = 10
        
        cart.save()
        
        cartDatas = CartModel.objects.filter(usercart =user)
        
        return render(request, "cart.html", {"title": "cart:)",
                                             "cartDatas": cartDatas,
                                             "cart": True})
        
class CartdelView(LoginRequiredMixin, View):
    login_url= "/login/"
    
    def post(self, request, *args, **kwargs):
        pid=request.POST.get("pid")
        cart = CartModel.objects.get(usercart_id=request.user.id, productcart_id=pid)
        cart.delete()
        return redirect(reverse("cartview"))
    
class OrderView(LoginRequiredMixin, View):
    login_url= "/login/"
    
    def get(self, request, *args, **kwargs):
        
        orders = OrdersModel.objects.filter(orderuser = request.user)
            
        return render(request, "orders.html", {"title": "orders",
                                               "user": request.user,
                                               "orders": orders})

    def post(self, request, *args, **kwargs):
        adressdata = UserdataModel.objects.filter(datauser=request.user).first()
        if adressdata:
            pass
        else:
            return redirect(reverse("profile"))
        
        product = CartModel.objects.filter(usercart=request.user)
        
        with transaction.atomic():
            for item in product:
                OrdersModel.objects.create(orderuser=request.user, 
                                           orderproduct=item.productcart,
                                           ordercount=item.countval)
                item.delete()
        
        orders = OrdersModel.objects.filter(orderuser = request.user)
            
        return render(request, "orders.html", {"title": "orders",
                                               "user": request.user,
                                               "orders": orders})

class ReviewView(LoginRequiredMixin, View):
    login_url= "/login/"
    
    # def get(self, request, *args, **kwargs):
    #     product = ProductData.objects.all()
    #     revies = ReviewModel.objects.filter(reviewuser=request.user)
    #     return render(request, "index.html")
    
    def post(self, request, *args, **kwargs):
        pid = request.POST.get("pid")
        rating = request.POST.get("rating")
        review = request.POST.get("review")
        product = ProductData.objects.get(id=pid)
        
        review = ReviewModel.objects.filter(reviewuser=request.user, reviewproduct=product).first()
        
        if review:
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                edited = form.save(commit=False)
                edited.reviewuser = request.user
                edited.reviewproduct = product
                edited.save()
            
        else:
            ReviewModel.objects.create( reviewuser=request.user, 
                                        reviewproduct=product, 
                                        rating=rating, 
                                        review=review)
        return redirect(reverse('orders'))
    