from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(
        verbose_name="Номер телефона", null=False, blank=False, max_length=11
    )

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Address(models.Model):
    city = models.CharField(
        verbose_name="Город", null=False, blank=False, max_length=100
    )
    street = models.CharField(
        verbose_name="Улица", null=False, blank=False, max_length=100
    )
    house = models.CharField(verbose_name="Дом", max_length=10, null=False, blank=False)
    entrance = models.IntegerField(verbose_name="Подъезд", null=False, blank=False)
    apartment = models.IntegerField(verbose_name="Квартира", null=False, blank=False)

    user = models.OneToOneField(
        "User", null=True, verbose_name="Пользователь", on_delete=models.RESTRICT
    )

    def __str__(self):
        return (
            f"г. {self.city}, ул. {self.street}, д. {self.house}, кв-{self.apartment}."
        )

    class Meta:
        db_table = "addresses"
        verbose_name = "Адрес доставки"
        verbose_name_plural = "Адреса доставки"


class Product(models.Model):
    name = models.CharField(
        verbose_name="Наименование", null=False, blank=False, max_length=100
    )
    price = models.FloatField(verbose_name="Цена", blank=False, null=False)
    count = models.IntegerField(
        verbose_name="Количество товара", null=False, blank=False
    )

    class Meta:
        db_table = "products"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class OrderStatus(models.Model):
    name = models.CharField(
        verbose_name="Название", null=False, blank=False, max_length=20
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "order_statuses"
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статусы заказов"


class Bucket(models.Model):
    user = models.ForeignKey(
        "User", verbose_name="Пользователь", on_delete=models.RESTRICT
    )
    product = models.ForeignKey(
        "Product", verbose_name="Товар", on_delete=models.RESTRICT
    )

    class Meta:
        db_table = "buckets"
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"


class Order(models.Model):
    order_date = models.DateTimeField(
        null=False, blank=False, verbose_name="Дата заказа", auto_now_add=True
    )
    customer_name = models.CharField(
        null=False,
        blank=False,
        verbose_name="Имя заказчика",
        default="",
        max_length=100,
    )
    date_receiving = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата получения"
    )
    phone = models.CharField(
        verbose_name="Номер мобильного телефона", max_length=11, null=False, blank=False
    )
    status = models.ForeignKey(
        "OrderStatus",
        null=False,
        blank=False,
        verbose_name="Статус заказа",
        on_delete=models.RESTRICT,
    )
    address = models.ForeignKey(
        "Address", null=False, verbose_name="Адрес досатвки", on_delete=models.RESTRICT
    )

    class Meta:
        db_table = "orders"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class ProductOrder(models.Model):
    product = models.ForeignKey(
        "Product",
        on_delete=models.RESTRICT,
        verbose_name="Товар",
        null=False,
        blank=False,
    )
    order = models.ForeignKey(
        "Order",
        on_delete=models.RESTRICT,
        verbose_name="Заказ",
        null=False,
        blank=False,
        related_name="products_orders",
    )
    count = models.IntegerField(verbose_name="Количество", null=False, default=1)
    price = models.FloatField(null=False, blank=False, verbose_name="Цена")

    class Meta:
        db_table = "products_orders"
        verbose_name = "товар в заказе"
        verbose_name_plural = "Товары в заказах"
