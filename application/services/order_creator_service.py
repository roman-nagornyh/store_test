from application.models import Address, User, ProductOrder, Product
from application.forms import AddressForm, OrderForm, BaseOrderForm
from django.forms import ModelForm
from django.db import transaction
from django.db.models.aggregates import Count


class OrderCreatorService:
    def __init__(self, data, user: User, selected_products: list[int] = None):
        self._data = data
        self._user = user
        self._selected_products = selected_products

    def _get_products(self):
        if not self._user.is_authenticated:
            products = Product.objects.filter(pk__in=set(self._selected_products))
            for product in products:
                product.len = self._selected_products.count(product.pk)
        else:
            products = Product.objects.filter(bucket__user_id=self._user.pk).annotate(
                len=Count("pk", distinct=True)
            )
        return products

    def _get_or_create_address(self) -> int | BaseOrderForm:
        address_form = AddressForm(data=self._data)
        if (
            self._user.is_authenticated
            and Address.objects.filter(user_id=self._user.pk).exists()
        ):
            return self._user.address.pk
        elif address_form.is_valid():
            return AddressForm(data=self._data).save().pk
        return address_form

    def _create_order(self, address_id: int) -> int | BaseOrderForm:
        order_form = OrderForm(data=self._data)
        order_form.status = 1
        order_form.address = address_id
        if order_form.is_valid():
            return order_form.save().pk
        else:
            return order_form

    @transaction.atomic()
    def create(self) -> bool | BaseOrderForm:
        products = self._get_products()
        address = self._get_or_create_address()
        if isinstance(address, BaseOrderForm):
            return address
        order = self._create_order(address)
        if isinstance(order, BaseOrderForm):
            return order
        order_products = [
            ProductOrder(
                order_id=order,
                product_id=product.pk,
                price=product.price,
                count=product.len,
            )
            for product in products
        ]
        res = ProductOrder.objects.bulk_create(order_products)
        return True if len(res) > 0 else False
