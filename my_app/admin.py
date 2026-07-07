from django.contrib import admin
from .models import Category, Furniture, LikedFurniture, CartItem, ContactMessage, Order

admin.site.register([Category, Furniture, LikedFurniture, CartItem, ContactMessage, Order])
