from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
import uuid
from django.utils.deconstruct import deconstructible

User = get_user_model()

@deconstructible
class ImagePathGenerator:
    def __call__(self, instance, filename):
        path = f'media/product/{instance.product.user}/{instance.product.id}/image/{filename}'
        return path
image_path = ImagePathGenerator()

class Category(models.Model):
    name = models.CharField(max_length=100)
    on_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    on_create = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    public_id = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to=image_path)

    class Meta:
        unique_together = ['product', 'image']

class Comment(models.Model):
    comment_text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username}"

class ShoppingList(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f'{self.user.username}_shoppinglist'

class ShoppingListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['shopping_list', 'product']

class Commande(models.Model):
    shopping_list = models.OneToOneField(ShoppingList, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class CommandeProduct(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ['commande', 'product']