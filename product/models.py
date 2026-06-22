from django.db import models
import uuid 
from authenticate.models import User
# Create your models here.

class ProductAlbum(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

MEDIA_TYPE = [
    ("IMAGE", "Image"),
    ("VIDEO", "Video")
]
class Media(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    file = models.FileField(upload_to="product")
    type = models.CharField(max_length=5, choices=MEDIA_TYPE, default=MEDIA_TYPE[0][0])
    album = models.ForeignKey(ProductAlbum, on_delete=models.CASCADE, related_name="album")

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    expire_at = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    quantity_sold = models.PositiveIntegerField(default=0)
    description = models.TextField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product")
    weight = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to="product")
    album = models.ForeignKey(ProductAlbum, on_delete=models.SET_NULL, null=True, blank=True, related_name="product_album")
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)


class Sale(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    total_amount = models.PositiveBigIntegerField()
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                  blank=True, related_name="buyer_sales")
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

class ProductSale(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_sale_record")
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="sale_product")
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()        