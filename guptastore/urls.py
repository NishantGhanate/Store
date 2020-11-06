from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   
    # CRUD OPS FOR ADMIN / STAFF 
    path('store/add_product', views.add_product, name='add_product'),
    path('store/add_product/<int:id>/add_productinfo', views.add_productinfo, name='add_productinfo'),
    path('store/delete_product/<int:id>', views.delete_product, name='delete_product'),

    path('store/add_brand', views.add_brand, name='add_brand'),
    path('store/delete_brand/<int:id>', views.delete_brand, name='delete_brand'),

    path('store/add_category', views.add_category, name='add_category'),
    path('store/delete_category/<int:id>', views.delete_category, name='delete_category'),
    path('store/add_category/<int:cid>/add_subcategory', views.add_subcategory, name='add_category'),
    path('store/delete_subcategory/<int:id>', views.delete_subcategory, name='delete_subcategory'),


    # Show all products / new added / sales etc
    path('', views.home, name='home'),
    
    # Browse by catergory 
    path('category', views.cateogry, name='cateogry'),
    path('category/<int:id>/', views.get_subcategory, name='get_subcategory'),
    path('category/<int:cid>/subcategory/<int:sid>/', views.sub_category, name='sub_cateogry'),

    # Browse by brand

    # Shopping cart
    path('cart/', views.cart, name='cart'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_no>', views.get_order, name='get_order'),
    path('update_item/', views.update_item, name='update_item'),
    path('checkout_order', views.checkout, name='checkout'),

    path('signin', views.signin, name='signin'),
    path('login', views.loginPage, name='loginPage'),
    path('logout', views.logoutPage , name = 'logoutPage'),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='store/reset_password.html'), name='reset_password'),
    path('reset_password_done/',auth_views.PasswordResetDoneView.as_view(template_name='store/reset_password_done.html') , name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='store/password_reset_confirm.html') , name='password_reset_confirm'),
    path('resest_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='store/resest_password_complete.html') , name='password_reset_complete'),

    # Analytics 
    
]