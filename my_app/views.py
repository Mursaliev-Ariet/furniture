from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .serializers import *
from django.db import transaction
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(parent__isnull=True)  # только корневые
    serializer_class = CategorySerializer
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
class FurnitureListCreateView(generics.ListCreateAPIView):
    queryset = Furniture.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FurnitureListSerializer
        return FurnitureSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        material = self.request.query_params.get('material')
        season = self.request.query_params.get('season')
        popular = self.request.query_params.get('popular')
        new = self.request.query_params.get('new')

        if category:
            queryset = queryset.filter(category_id=category)
        if material:
            queryset = queryset.filter(material__icontains=material)
        if season:
            queryset = queryset.filter(season=season)
        if popular is not None:
            queryset = queryset.filter(is_popular=popular.lower() == 'true')
        if new is not None:
            queryset = queryset.filter(is_new=new.lower() == 'true')

        return queryset
class FurnitureDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_favorites(request):
    favorites = LikedFurniture.objects.filter(user=request.user)
    serializer = LikedFurnitureSerializer(favorites, many=True)
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_favorite(request, furniture_id):
    furniture = get_object_or_404(Furniture, id=furniture_id)
    favorite, created = LikedFurniture.objects.get_or_create(
        user=request.user,
        furniture=furniture
    )
    if not created:
        favorite.delete()
        return Response({'status': 'removed'}, status=status.HTTP_200_OK)
    return Response({'status': 'added'}, status=status.HTTP_201_CREATED)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    serializer = CartItemSerializer(cart_items, many=True)
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    serializer = CartItemCreateSerializer(data=request.data)
    if serializer.is_valid():
        furniture = get_object_or_404(Furniture, id=serializer.validated_data['furniture'])
        quantity = serializer.validated_data['quantity']
        size = serializer.validated_data.get('size', '')

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            furniture=furniture,
            size=size,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({'status': 'added', 'quantity': cart_item.quantity},
                       status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    quantity = request.data.get('quantity')
    if quantity is None:
        return Response({'error': 'quantity required'}, status=status.HTTP_400_BAD_REQUEST)

    if quantity <= 0:
        cart_item.delete()
        return Response({'status': 'deleted'}, status=status.HTTP_200_OK)

    cart_item.quantity = quantity
    cart_item.save()
    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data)
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return Response({'status': 'deleted'}, status=status.HTTP_204_NO_CONTENT)
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def clear_cart(request):
    CartItem.objects.filter(user=request.user).delete()
    return Response({'status': 'cleared'}, status=status.HTTP_204_NO_CONTENT)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_orders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_order(request):
    with transaction.atomic():
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order = serializer.save(user=request.user)

        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                furniture=item.furniture,
                quantity=item.quantity,
                price_at_time=item.furniture.price,
                size=item.size
            )

        cart_items.delete()
        order.calculate_total()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class ApplicationListCreateView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return Application.objects.filter(is_processed=False)
class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer