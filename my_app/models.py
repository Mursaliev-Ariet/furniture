from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    icon = models.CharField(max_length=10, default='🛏️', verbose_name="Иконка (эмодзи)")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Родительская категория"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['order']


class Document(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    number = models.CharField(max_length=50, verbose_name="Номер")
    description = models.TextField(blank=True, verbose_name="Описание")
    file = models.FileField(upload_to='documents/', blank=True, null=True, verbose_name="Файл")
    furniture = models.ForeignKey(
        'Furniture',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents',
        verbose_name="Товар"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents',
        verbose_name="Категория"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return f"{self.title} №{self.number}"


class Furniture(models.Model):
    SEASON_CHOICES = [
        ('winter', 'Зима'),
        ('summer', 'Лето'),
        ('all', 'Всесезонный'),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='furniture',
        verbose_name="Категория"
    )
    name = models.CharField(max_length=200, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    material = models.CharField(max_length=100, verbose_name="Материал")  # ткань
    color = models.CharField(max_length=50, verbose_name="Цвет")
    sku = models.CharField(max_length=50, verbose_name="Артикул")
    description = models.TextField(verbose_name="Описание комплектации")
    care_instructions = models.TextField(verbose_name="Рекомендации по уходу")
    sizes = models.JSONField(default=list, verbose_name="Размеры")  # список строк: ['1,5 сн', '2 сн', ...] или ['40', '42', ...]
    season = models.CharField(max_length=10, choices=SEASON_CHOICES, default='all', verbose_name="Сезон")
    is_popular = models.BooleanField(default=False, verbose_name="Популярный")
    is_new = models.BooleanField(default=False, verbose_name="Новинка")
    image_color = models.CharField(max_length=20, default='#e8ddd2', verbose_name="Цвет фона")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class LikedFurniture(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return f"{self.user.username} - {self.furniture.name}"


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=20, blank=True, verbose_name="Выбранный размер")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f"{self.furniture.name} ({self.size})"

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
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.CharField(max_length=200, verbose_name="Организация")
    contact_name = models.CharField(max_length=100, verbose_name="Контактное лицо")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=200, verbose_name="Улица")
    house = models.CharField(max_length=20, verbose_name="Дом")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Сумма заказа")
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Стоимость доставки")
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        total = sum(item.total_price for item in self.items.all())
        self.total_amount = total + self.delivery_cost
        self.save()
        return self.total_amount

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.id} от {self.created_at.strftime('%d.%m.%Y')}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена на момент заказа")
    size = models.CharField(max_length=20, blank=True, verbose_name="Размер")

    @property
    def total_price(self):
        return self.price_at_time * self.quantity

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"


class Application(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    furniture = models.ForeignKey(Furniture, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Интересующий товар")
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"Заявка от {self.name} ({self.phone})"