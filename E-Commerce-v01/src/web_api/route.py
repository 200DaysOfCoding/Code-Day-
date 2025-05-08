from rest_framework import routers
from .viewsets import CategoryModelViewSet, ProductModelViewSet, ProuctImageModelViewSet, \
    Product_and_List_ImageModelViewSet, ProductCreate_and_ImageList_ModelViewSet, ShoppingListModelViewSet, \
    ShoppingListItemModelViewSet

router = routers.DefaultRouter()
router.register('category', CategoryModelViewSet, basename='category')
router.register('product', ProductModelViewSet, basename='product')
router.register('product-image', ProuctImageModelViewSet, basename='product-image')
router.register('product-register', ProductCreate_and_ImageList_ModelViewSet, basename='product-list-image')
router.register('product-list', Product_and_List_ImageModelViewSet, basename='product-list')
router.register('ShoppingList', ShoppingListModelViewSet, basename='ShoppingList')
router.register('ShoppingListItemModelViewSet', ShoppingListItemModelViewSet, basename='ShoppingListItemModelViewSet')
