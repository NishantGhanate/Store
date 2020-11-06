from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework import permissions
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework import generics


from .models import * 
from .serializers import *


@api_view(['GET'])
def apiOverview(request):
    urls = {
        'List'   : '/product-list',
        'Detail' : '/product-detail',
        'Create' : '/product-create',
        'Brand'  : '/brands-list'
    }
    return Response(urls)

@api_view(['GET'])
def productList(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['GET','DELETE'])
@permission_classes((IsAuthenticated,IsAdminUser ))
def productDetial(request,pk):
    try:
        product = Product.objects.get(id=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        product.delete()
        return HttpResponse(status=204)

@api_view(['POST'])
@permission_classes((IsAuthenticated,IsAdminUser ))
def productCreate(request):
    serializer = ProductSerializer(data=request.data)
    print(serializer)
    # product = Product.objects.get(id=pk)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def brandList(request):
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands,many=True)
    return Response(serializer.data)

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'brand','manufacture','product_info__price']