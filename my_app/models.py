from django.db import models
from django.conf import settings
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "категории"
        verbose_name_plural = "категории"
        db_table = "категории"

class Furniture(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='furniture')
    name = models.CharField(max_length=200, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    material = models.CharField(max_length=100, verbose_name="Материал")
    color = models.CharField(max_length=50, verbose_name="Цвет")
    sku = models.CharField(max_length=50, verbose_name="Артикул")
    description = models.TextField(verbose_name="Описание комплектации")
    care_instructions = models.TextField(verbose_name="Рекомендации по уходу")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Мебель"
        verbose_name_plural = "Мебель"
        db_table = "Мебель"

class LikedFurniture(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        db_table = "Избранное"

    def __str__(self):
        return f"{self.user.username} - {self.furniture.name}"


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name='cartitem')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
        db_table = "cart_item"
    def __str__(self):
        return self.furniture.name
    @property
    def total_price(self):
        return self.furniture.price * self.quantity

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Сообщение контакта"
        verbose_name_plural = "Сообщения контактов"

    def __str__(self):
        return f"Сообщение от {self.name}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.CharField(max_length=200, verbose_name="Организация")
    contact_name = models.CharField(max_length=100, verbose_name="Контактное лицо")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=200, verbose_name="Улица")
    house = models.CharField(max_length=20, verbose_name="Дом")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"