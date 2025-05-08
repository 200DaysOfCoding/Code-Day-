from logging import raiseExceptions

from django.core.serializers import serialize
from django.db import transaction
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Product, Category, ProductImage, ShoppingList, ShoppingListItem, CommandeProduct, Commande, Comment
from .serializers import ProductModelSerializer, CategoryModelSerializer, ProductImageModelSerializer, \
    Product_and_List_ImageModelSerializer, ProductCreate_And_ImageList, ShoppingListModelSerializer,ShoppingListItemModelSerializer


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=kwargs.get('partial', False))

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProuctImageModelViewSet(ReadOnlyModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageModelSerializer


class Product_and_List_ImageModelViewSet(ModelViewSet):
    serializer_class = Product_and_List_ImageModelSerializer
    def get_queryset(self):
        return Product.objects.prefetch_related(
            Prefetch('product_images', queryset=ProductImage.objects.all())
        ).select_related('category', 'user').all()

    def perform_create(self, serializer):
        # Pour gérer la création avec images
        product = serializer.save()
        images = self.request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(product=product, image=image)

class ProductCreate_and_ImageList_ModelViewSet(ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreate_And_ImageList
        return ProductModelSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ShoppingListModelViewSet(ReadOnlyModelViewSet):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListModelSerializer

class ShoppingListItemModelViewSet(ModelViewSet):
    queryset = ShoppingListItem.objects.all()
    serializer_class = ShoppingListItemModelSerializer