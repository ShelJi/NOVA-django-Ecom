from django.db import models
from django.contrib.auth.models import User

import os
from datetime import datetime

def upload_to_timestamp(instance, filename):
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Split the filename to get the extension
    name, ext = os.path.splitext(filename)
    # Construct a new filename with timestamp
    new_filename = f"{timestamp}{ext}"
    # Return the full path where the file will be saved
    return os.path.join('images/', new_filename)

class UserdataModel(models.Model):
    profilestatus = models.BooleanField(default=False)
    datauser = models.ForeignKey( User, on_delete=models.CASCADE)
    contact = models.IntegerField( null=True)
    lmark = models.TextField(null=True)
    local = models.TextField(null=True)
    city = models.TextField(null=True)
    district = models.TextField(null=True)
    state = models.TextField(null=True)
    pincode = models.TextField(null=True)
    
    def __str__(self):
        return self.datauser.username

class ProductData(models.Model):

    choices = [("mobile","Mobile"),
               ("case","Case"),
               ("headphone","Headphone"),
               ("watch","Watch"),
               ("gadget","Gadget"),
               ("laptop","Laptop"),
               ("battery","Battery"),
               ("electronics","Electronics")]

    name = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=choices, default="electronics")
    color = models.CharField(max_length=50)
    actual_price = models.IntegerField()
    discount_price = models.IntegerField()
    stock = models.IntegerField()
    image1 = models.ImageField( upload_to=upload_to_timestamp)
    image2 = models.ImageField( upload_to=upload_to_timestamp)
    image3 = models.ImageField( upload_to=upload_to_timestamp)
    trending = models.BooleanField(default=False)
    
    def __str__(self):
        return self.category  +" - " + self.name
    
class ReviewModel(models.Model):
    RATING_CHOICES = [("0", "No ratings"),
                      ("1", "1 rating"),
                      ("2", "2 ratings"),
                      ("3", "3 ratings"),
                      ("4", "4 ratings"),
                      ("5", "5 ratings"),]
    
    reviewuser = models.ForeignKey( User, on_delete=models.CASCADE)
    reviewproduct = models.ForeignKey( ProductData, on_delete=models.CASCADE, null=True)
    rating = models.CharField( max_length=1, choices=RATING_CHOICES, default="0")
    review = models.TextField(null=True)

class CartModel(models.Model):
    usercart = models.ForeignKey( User, on_delete=models.CASCADE)
    productcart = models.ForeignKey(ProductData, on_delete=models.CASCADE)
    countval = models.IntegerField(default=1)
    
    def __str__(self):
        return f"User: {self.usercart.username}, Product: {self.productcart.name}, Count: {self.countval}"
    
class OrdersModel(models.Model):
    ORDER_STATUS = [("P", "pending"),
                    ("S", "shipped"),
                    ("D", "delivered"),
                    ("C", "cancelled")]
    
    orderuser = models.ForeignKey( User, on_delete=models.CASCADE)
    orderproduct = models.ForeignKey( ProductData, on_delete=models.SET_NULL, null= True)
    ordercount = models.IntegerField(default=1)
    orderdate = models.DateTimeField( auto_now_add=True)
    orderstatus = models.CharField( max_length=1, choices=ORDER_STATUS, default="P")
    
    def __str__(self):
        return f"User: {self.orderuser.username}, Product: {self.orderproduct.name}, Count: {self.ordercount}"


class LatestDeals(models.Model):
    carousel = models.ImageField(upload_to=upload_to_timestamp, default=None)