from itertools import product

from rest_framework.serializers import ModelSerializer
from .models import Category, Product, ProductImage, ShoppingList, ShoppingListItem
from rest_framework import serializers

class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductImageModelSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'category', 'user', 'price', 'on_create', 'quantity', 'public_id', )

#la vue qui renvoi les produits avec leur image
class Product_and_List_ImageModelSerializer(ModelSerializer):
    product_images = ProductImageModelSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ('name', 'category', 'user', 'price', 'on_create', 'quantity','product_images')

#la vue qui permèt de créer les produits avec plusieurs images
class ProductCreate_And_ImageList(ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True, required=False)

    class Meta:
        model = Product
        fields = ('name', 'category', 'user', 'price', 'on_create', 'quantity', 'images')

        extra_kwargs = {
            #'user': {'read_only': True},
            'on_create': {'read_only': True}
        }

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        print("IMAGES REÇUES :", images)  # 👀
        product = Product.objects.create(**validated_data)
        for image in images:
            ProductImage.objects.create(product=product, image=image)
            print("Image créée pour :", image)  # 👀
        return product

class ShoppingListModelSerializer(ModelSerializer):
    class Meta:
        model = ShoppingList
        fields ='__all__'

class ShoppingListItemModelSerializer(ModelSerializer):
    class Meta:
        model = ShoppingListItem
        fields ='__all__'
