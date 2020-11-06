from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from datetime import datetime



# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15 , null=True , blank=True)
    pincode = models.PositiveIntegerField(default=0)
    address = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.user  


class Category(models.Model):
    name =  models.CharField(max_length=100 , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.name  

# Category child model 
class CategorySub(models.Model):
    category =  models.ForeignKey(Category,null=True,on_delete=models.CASCADE)
    name =  models.CharField(max_length=100 , null=True , blank=True)
    image_url = models.CharField(max_length=300 , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.name  

class Brand(models.Model):
    name =  models.CharField(max_length=100 , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.name  

class ProductImage(models.Model):
    image_url = models.CharField(max_length=300 , null=True , blank=True)
    image = models.ImageField(null=True , blank=True)

    def __str__(self):
        return "%s" % self.image_url  

class Product(models.Model):
    name = models.CharField(max_length=100 , null=True , blank=True)
    brand = models.ForeignKey(Brand,null=True,on_delete=models.SET_NULL)
    manufacture = models.CharField(max_length=100 , null=True , blank=True)
    product_image = models.CharField(max_length=300 , null=True , blank=True)
    sub_category = models.ForeignKey(CategorySub,null=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "%s" % self.name  


# Product child model 
class ProductInfo(models.Model):
    product_id = models.ForeignKey(Product,null=True,on_delete=models.CASCADE ,related_name='product_info')
    weight = models.CharField(max_length=100 , null=True , blank=True)
    price =  models.FloatField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    stock = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['product_id', 'price']
        ordering = ['product_id']

    def __str__(self):
        return '%s , Rs %d' % (self.product_id,self.price)

    
class Order(models.Model):
    STATUS_CHOICES = (
    ('b', 'Booked'),    
    ('p', 'Pending'),
    ('o', 'Out for delivery'),
    ('c', 'Completed'),
    ) 
    customer = models.ForeignKey(Customer,related_name='order',on_delete=models.SET_NULL , blank=True,null=True)
    order_no =  models.CharField(max_length=20 , blank=True,null=True  )
    checkout = models.BooleanField(default=False)
    status = models.CharField(max_length=20 , choices=STATUS_CHOICES, default='b')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'order no :%s ' %  self.order_no

    @property
    def get_cart_total(self):
        orderitem = self.orderitem_set.all()
        return sum([item.get_total for item in orderitem])
        

    @property
    def get_cart_quantity(self):
        orderitems = self.orderitem_set.all()
        return sum([item.quantity for item in orderitems])

# Item in cart 
class OrderItem(models.Model):
    product = models.ForeignKey(ProductInfo,on_delete=models.SET_NULL , blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL , blank=True,null=True)
    price = models.PositiveIntegerField(default=0 , blank=True,null=True)
    quantity = models.PositiveIntegerField(default=0 , blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Product id :%s ' %  self.product
    
    @property
    def get_total(self):
        return self.price * self.quantity

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL , blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL , blank=True,null=True)
    name = models.CharField(max_length=100 , null=True , blank=True)
    phone = models.CharField(max_length=20 , null=True , blank=True)
    address = models.CharField(max_length=200 , null=True , blank=True)
    pincode = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'address  :%s ' %  self.address

class Delivery(models.Model):
    min_order = models.PositiveIntegerField(default=0)
    delivery_charge = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)