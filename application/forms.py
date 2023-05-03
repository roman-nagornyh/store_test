from django import forms
from application.models import Order, Address


class BaseOrderForm(forms.ModelForm):
    form_key = ""


class OrderForm(BaseOrderForm):
    form_key = "order_form"

    class Meta:
        model = Order
        fields = ("customer_name", "phone", "status", "address")


class AddressForm(BaseOrderForm):
    form_key = "address_form"

    class Meta:
        model = Address
        fields = "__all__"
