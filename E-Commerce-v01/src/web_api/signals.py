from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ShoppingList


@receiver(post_save, sender=get_user_model())
def create_shopping_list(sender, instance, created, **kwargs):
    if created:
        ShoppingList.objects.create(user=instance)