from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview' ),
    path('product-list/', views.productList, name='product-list' ),
    path('product-detail/<int:pk>', views.productDetial, name='product-detail' ),
    path('product-create/', views.productCreate, name='product-create' ),
    
    path('brands-list/', views.brandList, name='brand-list' ),
]
