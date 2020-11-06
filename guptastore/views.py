from django.shortcuts import render , redirect , get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth import authenticate , login ,logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group , User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db.models import Q
from django.db.models import Prefetch

from api.models import * 
from api.forms import *
from .decoraters import * 

import json
import random
import string


@login_required(login_url='loginPage')
@admin_only
def add_brand(request):
    context = {}
    context['redirect']  = "/store/add_brand"
    if request.method == "GET":
        brands =  Brand.objects.all().order_by('created_at')
        paginator = Paginator(brands, 10)
        page = request.GET.get('page', 1)
        try:
            brands = paginator.page(page)
        except PageNotAnInteger:
            brands = paginator.page(1)
        except EmptyPage:
            brands = paginator.page(paginator.num_pages)
        context['brands'] =brands
        return render(request,'store/add_brand.html',context)
        
    elif request.method == "POST" and request.is_ajax():
        if request.POST.get('id'):
            instance = get_object_or_404(Brand,id=request.POST.get('id'))
            form = BrandForm(request.POST , instance=instance)
        else:
            form = BrandForm(request.POST)     
        if form.is_valid:
            instance = form.save()
            context['ser_instance']  = serializers.serialize('json', [ instance, ])
            return JsonResponse(context, status=200)
        else:
            context['error'] = form.errors
            return JsonResponse(context, status=400)


@login_required(login_url='loginPage')
@admin_only
def delete_brand(request,id):
    context = {}
    context['redirect']  = "/store/add_brand"
    if request.method== "DELETE" and request.is_ajax():
        print(id)
        try :
            brand = Brand.objects.get(pk=id)
            brand.delete()
        except ObjectDoesNotExist as e:
            context['error'] = e
    return JsonResponse(context)
    
@login_required(login_url='loginPage')
@admin_only
def add_category(request):
    context = {}
    context['redirect']  = "/store/add_category"
    if request.method == "GET":
        context['categories'] = Category.objects.all()
        return render(request,'store/add_category.html',context)
    elif request.method == "POST" and request.is_ajax():
        id = request.POST.get('id')
        name = request.POST.get('name')
        if id:
            try :
                cateogry = Category.objects.get(pk=id)
                cateogry.name = name 
                cateogry.save()
            except ObjectDoesNotExist as e:
                context['error'] = e
        else:
            cateogry = Category(name=name)
            cateogry.save()
        return JsonResponse(context)

@login_required(login_url='loginPage')
@admin_only
def delete_category(request,id):
    context = {}
    context['redirect']  = "/store/add_category"
    if request.method== "DELETE" and request.is_ajax():
        print(id)
        try :
            category = Category.objects.get(pk=id)
            category.delete()
        except ObjectDoesNotExist as e:
            context['error'] = e
    return JsonResponse(context)

@login_required(login_url='loginPage')
@admin_only
def add_subcategory(request,cid):
    context = {}
    context['redirect']  = "/store/add_category/{id}/add_subcategory".format(id=cid)
    category = Category.objects.get(pk=cid)
    print(category)
    if request.method == "GET":
        context['subcategories']  = CategorySub.objects.filter(category=category)
        return render(request,'store/add_subcategory.html',context)
    elif request.method == "POST" and request.is_ajax():
        id =  request.POST.get('id')
        name = request.POST.get('name')
        print(id,name)
        if id:
            try :
                sub_category = CategorySub.objects.get(pk=id)
                sub_category.name = name 
                sub_category.save()
            except ObjectDoesNotExist as e:
                context['error'] = e
        else:
            sub_category = CategorySub(category=category,name=name)
            sub_category.save()
        return JsonResponse(context)
       
@login_required(login_url='loginPage')
@admin_only
def delete_subcategory(request,id):
    context = {}
    if request.method== "DELETE" and request.is_ajax():
        try :
            subcategory = CategorySub.objects.get(pk=id)
            context['redirect']  = "/store/add_category/{id}/add_subcategory".format(id=subcategory.category.id)
            subcategory.delete()
        except ObjectDoesNotExist as e:
            context['error'] = e
    return JsonResponse(context)
    

@login_required(login_url='loginPage')
@admin_only
def add_product(request):
    """
    // Todo :
    1 - Get all previous products for option list render 
    2 - On Post request check if id is present if not create new product 
    3 - Get sub-product list and add product forgien key relations
    4) Get product_info id & fetch details to render / handle exception
    5) On post request form sanitize and update and send back data
    6) On Delete & ajax request delete product and send store redirect url
    """
    context = {}
    
    if request.method == "GET":
        context['products'] =  Product.objects.all()
        return render(request,'store/add_product.html',context)

    elif request.method == "POST" and request.is_ajax():
        # print(request.POST)
        context['redirect']  = "/store/add_product"
        product_id =  request.POST.get('id')
        product = None
        if product_id:
            try :
                form = ProductForm(request.POST.copy())
                # save changes
                if form.is_valid():
                    product = Product.objects.get(pk=product_id)
                    product = form.data
                    product.save()
                    return JsonResponse(context)
                else:
                    context['error'] = form.errors
                    return JsonResponse(context) 
            except ObjectDoesNotExist as e:
                context['error'] = e
                return JsonResponse(context)
        else:
            data = request.POST.copy()
            brand = Brand.objects.get(name=data.brand)
            sub_category = CategorySub.objects.get(name=data.sub_category)
            product = Product(name=data.name , brand=brand ,
                    product_image=data.product_image , sub_category=sub_category,
                    manufacture='')
            product.save()
            
             
            # form = ProductForm(product_data)
            # print(product_data)
            # form.save()
            # if form.is_valid():
            #     form.save()
            #     return JsonResponse(context)
            # else:
            #     #  return form error
            #     context['error'] = form.errors
            #     print(form.errors)
            #     return JsonResponse(context)    
   
@login_required(login_url='loginPage')
@admin_only
def delete_product(request,id):
    context = {}
    context['context'] = '/store/add_product'
    try:
        product = Product.objects.get(pk=id)
        product.delete()
        return JsonResponse(context)
    except ObjectDoesNotExist as e :
        context['error'] = e
        return render(request,'store/product_notfound.html',context)


def add_productinfo(request,id):
    pass


def delete_productinfo(request,id):
    if request.method == "POST":
        form = ProductInfoForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            # product.image_url =  data.image_url
            product.weight = data.weight
            product.price =  data.price
            product.quantity = data.quantity
            product.stock = data.stock 
            product.save()
            return redirect("/store/edit_product/"+id)
        else:
            context['form'] = form

    elif request.method== "DELETE" and request.is_ajax():
        try:
            product.delete()
            return JsonResponse({"redirect": "/store"})
        except :
            return JsonResponse({"error": "Exception occured "})

    context['product'] = product
    return render(request,'store/edit_product.html',context)



# Create your views here.
def home(request):
    context = {}
    """
    // Todo : 
    1)
    2) handle categoery query & product search on that
    """ 
    context['products'] =  Product.objects.all()
    
    return render(request,'store/store.html',context)

def autocomplete(request):
    if request.is_ajax():
        queryset = Product.objects.filter(name__startswith=request.GET.get('search', None))
        plist = []        
        for i in queryset:
            plist.append(i)
        data = {
            'list': plist,
        }
        return JsonResponse(data)

def cateogry(request):
    pass

def get_subcategory(request,id):
    context = {}
    try:
        # cateogry = Category.objects.get(pk=id)
        sub_category = CategorySub.objects.filter(category__id=id)    
    except ObjectDoesNotExist as o:
        context['error'] = o
        return render(request,'store/invalid.html',context)
    context['sub_cateogry'] = sub_category
    return render(request,'store/category.html',context)

def sub_category(request,cid,sid):
    context = {}
    products = Product.objects.filter(sub_category__id=sid)
    print(products)
    context['products'] = products
    return render(request,'store/store.html',context)

def store(request):
    """
    // Todo : 
    1) Get all products and display in card/title
    2) Get query on product name / brand / cateogry
    3) Products pagination

    """
    query = request.GET.get('query')
    if query:
        # products = Product.objects.prefetch_related('product_id__product')
        products = ProductInfo.objects.filter( Q(product_id__name__icontains=query) | Q(product_id__brand__icontains=query)| Q(product_id__cateogry__icontains=query) )
    else:
        products = ProductInfo.objects.all()
    paginator = Paginator(products, 9)
    page = request.GET.get('page', 1)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
 
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'products' : products
    }
    return render(request,'store/store.html',context)

def cart(request):
    """
    // Todo : 
    1) Check user auth status 
    2) Create empty cart or fetch previous unfinised cart items
    3) Render items in cart page

    """
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer,checkout=False)
        items = order.orderitem_set.all()
    else:
        try :
            cart = json.loads(request.COOKIES['cart'])
        except :
            cart = {}
        print('Cart : ' , cart)
        items = []
        order = {'get_cart_items': 0, 'get_cart_total' : 0 }
        cartItems = order['get_cart_items']
        for i in cart:
            cartItems += cart[i]['quantity']
            product = ProductInfo.objects.get(id=i)
            total = ( product.price * cart[i]['quantity'])
            order['get_cart_toal'] += total
            order['get_cart_items'] += cart[i]['quantity']
            item = {
                'product':{
                    'id' : product.id,
                    'name':product.name,
                    'price': product.price,
                    'image' : product.image,
                },
                'quantity' : cart[i]['quantity'],
                'get_total' : total,
            }
            items.append(item)
    context = {
        'items' : items,
        'order' : order
    }
    return render(request,'store/cart.html',context)

def update_item(request):
    """
    // Todo : 
    1) Update the cart add / remove / delete
    2) Fetch product id to update cart items i.e ( qt , price , total price = qt x price )
    3) Constraint requested qt < actual qt 

    """
    if request.method == 'POST':
        data = json.loads(request.body)
        product_info_id = data['product_id']
        action = data['action']
        customer = request.user.customer
        product = ProductInfo.objects.get(id=product_info_id)
        order , created = Order.objects.get_or_create(customer=customer,checkout=False)
        orderItem , created = OrderItem.objects.get_or_create(order=order , product=product)
        if created:
            orderItem.price = product.price
        if action == 'add':
            if orderItem.quantity >= product.quantity :
                orderItem.quantity = product.quantity
            else:
                orderItem.quantity +=1
        elif action == 'remove':
            orderItem.quantity -=1
        elif action == 'delete':
            orderItem.quantity = 0

        orderItem.save()

        if  orderItem.quantity <= 0 :
            orderItem.delete()
        
        data = {
            'order_total'   : order.get_cart_total,
            'order_quantity': order.get_cart_quantity,
            'item_total'    : orderItem.get_total,
            'item_quantity' : orderItem.quantity,
            'action'   : data['action']
        }
        return JsonResponse(data,safe=False)
    else:
        return JsonResponse("OOO HACKER HELP !!",safe=False)

def get_orderno():
    return ''.join(random.choices(string.digits, k=8))
    
def checkout(request):
    """
    // Todo : 
    1) Fetch Cart items and render checkout form 
    2) Constraint Check delivery table for min order   / delivery charge
    3) If all well genereate Order no and store the order in db 

    """
    context = {}
    if request.method == 'GET':
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            order , created = Order.objects.get_or_create(customer=customer,checkout=False)
            context = {
                'customer' : customer,
                'order' : order,
            }
        return render(request,'store/checkout.html',context)

    elif request.method == 'POST':
        if request.user.is_authenticated:
            customer = request.user.customer
            order , created = Order.objects.get_or_create(customer=customer,checkout=False)
            order.order_no = get_orderno()
            order.checkout = True
            shippingForm =  ShippingForm(request.POST)
            if shippingForm.is_valid():
                form = shippingForm.save(commit=False)
                form.customer = customer
                form.order = order
                order.save()
                form.save()
                return redirect('home')
            else:
                context = {'errorMessages' : form.errors}
                return render(request,'store/checkout.html' , context )

def orders(request):
    """
    // Todo : 
    1) Fetch all the previous orders of customer
    2) Join query on order and product item info
    3) Orders pagination
    """
    if request.method == 'GET':
        if request.user.is_authenticated :
            if request.user.is_staff:
                orders = Order.objects.filter(checkout=True).prefetch_related('order_no__product').order_by('created_at')
            else :
                orders = Order.objects.filter(customer=request.user.customer , checkout=True).prefetch_related('order_no__product').order_by('created_at')
            paginator = Paginator(orders, 9)
            page = request.GET.get('page', 1)
            try:
                orders = paginator.page(page)
            except PageNotAnInteger:
                orders = paginator.page(1)
            except EmptyPage:
                orders = paginator.page(paginator.num_pages)
            context = {
                'orders' : orders
            }
    return render(request,'store/orders.html' , context )

@login_required(login_url='loginPage')
def get_order(request,order_no):
    """
    Todo : 
    1) Get order no  to display items that was in the cart 
    2) If staff login display all orders / if customters display only customers
    2) Expection handling on invalid orderno
    3) Pagintion not working :/
    4) Change Order status 
    """
    context = {}
    try:
        if request.user.is_staff:
            order = Order.objects.get(order_no=order_no)
            shipping = ShippingAddress.objects.get(order=order)
            context['form'] = OrderForm
            if request.method == "POST":
                status = request.POST.get('status')
                order.status = status
                order.save()
                return redirect('/orders/'+str(order_no))
        else:
            order = Order.objects.get(customer=request.user.customer ,order_no=order_no)
            shipping = ShippingAddress.objects.get(customer=request.user.customer ,order=order)
    except ObjectDoesNotExist as o:
        context['error'] = o
        return render(request,'store/invalid.html',context)
    # paginator = Paginator(order, 15)
    # page = request.GET.get('page', 1)
    # try:
    #     order = paginator.page(page)
    # except PageNotAnInteger:
    #     order = paginator.page(1)
    # except EmptyPage:
    #     order = paginator.page(paginator.num_pages)

    
    context['order'] = order
    context['shipping'] = shipping

    return render(request,'store/order_view.html',context)

@unauthenticatedUser
def loginPage(request):
    context = {}
    if request.method == 'GET':
        return render(request,'store/login.html' , context )
    elif request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('password')

        user = authenticate(request,username=username, password=pwd)
        if user is not None :
            login(request,user)
            if user.is_authenticated and user.is_staff:
                return redirect('home')
            elif user.is_authenticated :
                # usergroup = request.user.groups.values_list('name', flat=True).first()
                # if usergroup == "customer":
                return redirect('home')

        elif username is not None and pwd is not None:
            context = {'errorMessages' : 'Username or password incorrect'}
        return render(request,'store/login.html' , context )

@unauthenticatedUser
def signin(request):
    context = {}
    if request.method == 'GET':
        return render(request,'store/signin.html' , context )
    elif request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            userSigned = form.save(commit=True)
            group = Group.objects.get(name='customer')
            username = form.cleaned_data['username']
            userSigned.groups.add(group)
            customer = Customer()
            customer.user = userSigned
            customer.phone = ''
            customer.address = ''
            customer.save()
            messages.success(request,'Account created for ' + username)
            return redirect('loginPage')
        else:
            context = {'errorMessages' : form.errors}
            return render(request,'store/signin.html' , context )

@login_required(login_url='loginPage')
def logoutPage(request):
    logout(request)
    return redirect('home')

@login_required(login_url='loginPage')
@admin_only
def sales(request):
    pass

# @login_required(login_url='loginPage')
# @admin_only
# def sendEmail(userEmail,emailSubject,emailBody):
#     email = EmailMessage(
#             emailSubject,
#             emailBody,
#             'noreply@ktvwifi.com',
#             [userEmail],
#             )
#     email.send(fail_silently=False)
