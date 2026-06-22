from rest_framework import serializers
from product.models import Product, Sale, ProductSale

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    price = serializers.DecimalField(min_value=1, decimal_places=2, max_digits=10)
    weight = serializers.DecimalField(min_value=1, decimal_places=2, max_digits=10)
    expire_at = serializers.DateField(required=False)
    quantity = serializers.IntegerField(min_value=5)
    seller = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()
    images = serializers.ListField(
        child = serializers.ImageField(
            allow_empty_file = False
        ), 
        max_length=4,
        required=False,
        write_only=True
    )
    
    def get_seller(self, obj):
        return{
            "id": obj.seller.id,
            "firstname": obj.seller.lastname,
            "lastname": obj.seller.lastname,
            "profile_picture": obj.seller.profile_picture.url if obj.seller.profile_picture else None
        }
    def get_media(self, obj):
        media = obj.album.album.all()
        all_urls = [x.file.urls for x in media]
        return all_urls
    
    class Meta:
        model = Product
        fields = ["id", "name", "expire_at",
                  "price", "seller", "quantity", "description", "media",
                  "quantity_sold", "description", "images", "weight",
                  "created_at",
        ]
        read_only_fields = ["id", "quantity_sold", "seller", "created_at"
        ]

class ProductSalesSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)

    
class SaleSerializer(serializers.ModelSerializer):
    products = ProductSaleSerializer(many=True)
    class Meta:
        model = Sale 
        fields = ["id", "total_amount", "buyer", "created_at", "products"]
        read_only_fields = ["id", "total_amount", "buyer", "created_at"]



