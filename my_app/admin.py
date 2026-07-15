from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order']
    list_editable = ['icon', 'order']

@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_popular', 'is_new']
    list_editable = ['price', 'is_popular', 'is_new']
    filter_horizontal = []
    fields = ['category', 'name', 'price', 'material', 'color', 'sku', 'description',
              'care_instructions', 'sizes', 'is_popular', 'is_new', 'image_color']

@admin.register(LikedFurniture)
class LikedFurnitureAdmin(admin.ModelAdmin):
    list_display = ['user', 'furniture']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product_id', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['contact_name', 'organization', 'phone', 'email', 'city', 'created_at']
    readonly_fields = ['created_at']
