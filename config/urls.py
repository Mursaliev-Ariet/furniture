from django.contrib import admin
from django.urls import path
from my_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sale/", views.sale, name="sale"),
    path("favorite/<int:pk>/", views.add_to_favorite, name="favorite"),
    path("cart/<int:pk>/", views.add_to_cart, name="cart"),
]