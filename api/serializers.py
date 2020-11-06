from rest_framework import serializers
from .models import Product,ProductInfo,Brand,CategorySub


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields =  ('id','name')

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorySub
        fields =  ('id','name')


class ProductSerializer(serializers.ModelSerializer):
    # joinn query to fetch product remaining information 
    product_info = ProductInfoSerializer(many=True) 
    brand = BrandSerializer()
    sub_category = SubCategorySerializer()

    class Meta:
        model = Product
        fields = ('id', 'name','brand','sub_category','product_image','product_info')
        

