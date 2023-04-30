from django.core.management.base import BaseCommand
from application.models import Product, OrderStatus
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        product_list = []
        for i in range(1, 100):
            price = random.randint(1000, 100000)
            count = random.randint(10, 100)
            product_list.append(
                Product(name=f"Продукт {str(i)}", price=price, count=count)
            )
        Product.objects.bulk_create(product_list)
        OrderStatus.objects.create(name="Оформлен")
        OrderStatus.objects.create(name="Оплачен")
        OrderStatus.objects.create(name="Получен")
