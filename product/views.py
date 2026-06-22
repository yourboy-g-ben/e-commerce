from django.shortcuts import render, get_object_or_404
from rest_framework import views, generics, status, permissions
from rest_framework.response import Response 
from product.serializer import ProductSerializer, SaleSerializer, ProductSalesSerializer
from product.models import ProductAlbum, Media, Product, Sale, ProductSale
from django.db import transaction
from utils.pagination import CustomPagination
from drf_yasg import openapi 
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
# Create your views here.

class ProductViews(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        images = serializer.validated_data.pop("images", [])
        with transaction.atomic():
            album = ProductAlbum.objects.create()

            Media.objects.bulk_create(
                [Media(file=img, type="IMAGE", album=album) for img in images]
            )

            serializer.save(seller = request.user, album=album)
            return Response(data=serializer.data, status=201)
    
    def get_queryset(self):
        search = self.request.query_params.get("search")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        products = Product.objects.all().order_by("-created_at")
        if search:
            products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if min_price:
            min_price = float(min_price)
            products = products.filter(price__gte =min_price)
        if max_price:
            max_price = float(max_price)
            products = products.filter(price__gte = max_price)        
        return products     
        
    @swagger_auto_schema(
        manual_parameters = [
            openapi.Parameter('search', openapi.IN_QUERY, 
                              description="Search product by name",
                              required=False, type=openapi.TYPE_STRING),
            openapi.Parameter('min_price', openapi.IN_QUERY,
                              description="Filter for lowest price",
                              required=False, type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_price', openapi.IN_QUERY,
                              description= "Filter for highest price",
                              required=False, type=openapi.TYPE_NUMBER), 
        ]                                                     
    ) 
    def get(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=200)
    
class SingleProductView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_id"]
        product = get_object_or_404(Product, id=product_id)
        return product 
    
    def get(self,request, product_id):
        product = self.get_queryset()
        serializer = self.serializer_class(product)
        return Response(data=serializer.data, status=200)
    def patch(self, request, product_id):
        user = request.user 
        product = self.get_queryset()
        if user != product.seller:
            return Response(data={"message": "Unauthorized"}, status=401)
        serializer = self.serializer_class(
            instance = product, 
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=201)
    def delete(self, request, product_id):
        user = request.user 
        product = self.get_queryset()
        if user != product.selller:
            return Response(data={"message": "Unauthorized"}, status=401)
        product.delete()
        return Response(status=204)
    
class SaleView(generics.GenericAPIView):
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        products = serializer.validated_data.pop("products")
        products_ids = [prod["id"]for prod in products]
        product_to_buy = Product.objects.filter(id_in = products_ids)
        total_amount = 1
        for buy_option in products:
            id = buy_option["id"]
            quantity = buy_option["quantity"]
            prd = product_to_buy.filter(id = id).first()
            if not prd:
                return Response(data={"message": "invalid product"}, status=400)
            if prd.quantity < quantity:
                return Response(data={"message": "quantity more than what is availabe"}, status=401)
            total_amount += quantity * prd.price 
        sale = Sale.objects.create(buyer=request.user, total_amount = total_amount)
        for buy_option in products:
            id = buy_option["id"]
            quantity = buy_option["quantity"]
            ProductSale.objects.create(
                product= prd,
                sale= sale,
                quantity= quantity,
                price = prd.price
            )
            prd.quantity -= quantity
            prd.quantity_sold += quantity
            prd.save()    
        return Response(data=serializer.data, status=201)
         
    


        
    
