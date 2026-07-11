from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('furniture/', FurnitureListCreateView.as_view(), name='furniture-list'),
    path('furniture/<int:pk>/', FurnitureDetailView.as_view(), name='furniture-detail'),

    path('favorites/', get_favorites, name='favorites'),
    path('favorites/<int:furniture_id>/toggle/', toggle_favorite, name='toggle-favorite'),

    path('cart/', get_cart, name='cart'),
    path('cart/add/', add_to_cart, name='add-to-cart'),
    path('cart/<int:item_id>/', update_cart_item, name='update-cart-item'),
    path('cart/<int:item_id>/remove/', remove_from_cart, name='remove-from-cart'),
    path('cart/clear/', clear_cart, name='clear-cart'),

    path('orders/', get_orders, name='orders'),
    path('orders/create/', create_order, name='create-order'),

    path('applications/', ApplicationListCreateView.as_view(), name='applications'),
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),

    path('contact/', ContactMessageCreateView.as_view(), name='contact'),
]