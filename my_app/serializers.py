from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'order', 'parent', 'children']

    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class FurnitureSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Furniture
        fields = '__all__'

class FurnitureListSerializer(serializers.ModelSerializer):
    """Минимальный сериализатор для списка товаров"""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Furniture
        fields = ['id', 'name', 'price', 'category_name', 'material', 'season', 'sizes', 'is_popular', 'is_new', 'image_color']

class LikedFurnitureSerializer(serializers.ModelSerializer):
    furniture = FurnitureSerializer(read_only=True)

    class Meta:
        model = LikedFurniture
        fields = ['id', 'user', 'furniture']
        read_only_fields = ['user']

class CartItemSerializer(serializers.ModelSerializer):
    furniture = FurnitureSerializer(read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'furniture', 'quantity', 'size', 'total_price']
        read_only_fields = ['user']

class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['furniture', 'quantity', 'size']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество должно быть не менее 1")
        if value > 99:
            raise serializers.ValidationError("Максимальное количество - 99")
        return value

    def validate_size(self, value):
        furniture = self.initial_data.get('furniture')
        if furniture:
            try:
                furniture_obj = Furniture.objects.get(id=furniture)
                if value and value not in furniture_obj.sizes:
                    raise serializers.ValidationError(f"Размер {value} недоступен для этого товара")
            except Furniture.DoesNotExist:
                pass
        return value

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'
        read_only_fields = ['created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    furniture_name = serializers.CharField(source='furniture.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'furniture', 'furniture_name', 'quantity', 'price_at_time', 'size', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'status', 'total_amount']

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['organization', 'contact_name', 'phone', 'email', 'city', 'street', 'house', 'comment']

class ApplicationSerializer(serializers.ModelSerializer):
    furniture_name = serializers.CharField(source='furniture.name', read_only=True)

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['created_at', 'is_processed']