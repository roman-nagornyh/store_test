from django.views.generic import ListView, TemplateView, CreateView
from .models import Product, Bucket, Order, Address, ProductOrder
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from django.db.models import F
from django.db.models.aggregates import Count, Sum
from django.contrib.auth.views import LoginView


class ProductList(ListView):
    template_name = "products.html"
    model = Product
    queryset = Product.objects.all()
    paginate_by = 10


class BucketView(TemplateView):
    template_name = "buket.html"

    def get(self, request, *args, **kwargs):
        response = super(BucketView, self).get(request, *args, **kwargs)
        products = list()
        summ = 0
        if not request.user.is_authenticated and "products" in request.session:
            products = Product.objects.filter(pk__in=set(request.session["products"]))
            for product in products:
                pr_count = request.session["products"].count(product.pk)
                product.count = pr_count
                summ = summ + (pr_count * product.price)
        elif request.user.is_authenticated:
            products = (
                Bucket.objects.filter(user_id=request.user.id)
                .select_related("product")
                .values("product_id", "product__name", "product__price")
                .annotate(count=Count("product__id"))
            )
            summ = sum(x["product__price"] * x["count"] for x in products)
        if len(products) > 0:
            response.context_data["products"] = products
            response.context_data["sum"] = summ
        return response


class OrderListView(ListView):
    model = Order
    queryset = (
        Order.objects.select_related("status", "address")
        .prefetch_related("products_orders__product")
        .annotate(
            total_price=Sum(F("products_orders__price") * F("products_orders__count"))
        )
    )

    template_name = "orders/list.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(address__user_id=self.request.user.pk)
        elif "phone" in self.request.session:
            return self.queryset.filter(phone=self.request.session["phone"])


class OrderCreateView(CreateView):
    model = Order
    fields = ("phone", "address")
    template_name = "orders/create.html"
    queryset = Order.objects.all()

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        post = request.POST
        if (
            request.user.is_authenticated
            and Address.objects.filter(user_id=request.user.pk).exists()
        ):
            address = self.request.user.address
        else:
            address = Address.objects.create(
                city=post.get("city"),
                street=post.get("street"),
                house=post.get("house"),
                entrance=post.get("entrance"),
                apartment=post.get("apartment"),
                user_id=request.user.pk if request.user.is_authenticated else None,
            )
        order = Order.objects.create(
            phone=post.get("phone"),
            address_id=address.pk,
            status_id=1,
            customer_name=post.get("customer_name"),
        )
        products = list()
        if not request.user.is_authenticated:
            if "products" in request.session:
                session_products = request.session.pop("products")
                products = Product.objects.filter(pk__in=set(session_products))
                for product in products:
                    product.len = session_products.count(product.pk)
            request.session["phone"] = post.get("phone")
        else:
            products = Product.objects.filter(bucket__user_id=request.user.pk).annotate(
                len=Count("pk", distinct=True)
            )

        order_products = [
            ProductOrder(
                order_id=order.pk,
                product_id=product.pk,
                price=product.price,
                count=product.len,
            )
            for product in products
        ]
        _ = ProductOrder.objects.bulk_create(order_products)
        if len(_) == 0:
            raise Exception("Произошла ошибка")
        if request.user.is_authenticated:
            Bucket.objects.filter(user_id=request.user.pk).delete()
        return HttpResponseRedirect(redirect_to=reverse("application:order_list"))


def add_product_bucket(request, product_id):
    if not request.user.is_authenticated:
        if "products" in request.session:
            product_list = request.session["products"]
            product_list.append(product_id)
        else:
            product_list = [product_id]
        request.session["products"] = product_list
    else:
        user_id = request.user.pk
        Bucket.objects.create(user_id=user_id, product_id=product_id)
    return HttpResponseRedirect(redirect_to=reverse("application:products"))


class UserLogin(LoginView):
    template_name = "login.html"


def product_subtraction(request, product_id):
    if request.user.is_authenticated:
        Bucket.objects.filter(product_id=product_id).first().delete()
    else:
        if "products" in request.session:
            pr_list: list = request.session["products"]
            pr_list.remove(product_id)
            request.session["products"] = pr_list
    return HttpResponseRedirect(redirect_to=reverse("application:bucket"))


def product_delete(request, product_id):
    if request.user.is_authenticated:
        Bucket.objects.filter(product_id=product_id).delete()
    else:
        if "products" in request.session:
            request.session["products"] = [
                i for i in request.session["products"] if i != product_id
            ]
    return HttpResponseRedirect(redirect_to=reverse("application:bucket"))
