from application.models import Address, User, ProductOrder, Product, Bucket
from application.forms import AddressForm, OrderForm, BaseOrderForm
from django.forms import ModelForm
from django.db import transaction
from django.db.models.aggregates import Count
from django.http import QueryDict


class OrderCreatorService:
    def __init__(
        self, data: QueryDict, user: User, selected_products: list[int] = None
    ):
        self._data = data.dict()
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
        self._data.update({"status": 1, "address": address_id})
        order_form = OrderForm(data=self._data)
        if order_form.is_valid():
            return order_form.save().pk
        else:
            return order_form

    @transaction.atomic()
    def create(self) -> bool | list[BaseOrderForm]:
        products = self._get_products()
        address = self._get_or_create_address()
        errors_form = []
        if isinstance(address, BaseOrderForm):
            errors_form.append(address)
        order = self._create_order(address)
        if isinstance(order, BaseOrderForm):
            errors_form.append(order)
        if len(errors_form) > 0:
            return errors_form
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
        if self._user.is_authenticated:
            Bucket.objects.filter(user_id=self._user.pk).delete()
        return True if len(res) > 0 else False
