from django.views.generic import ListView, TemplateView
from .models import Product, Bucket, Order
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.db.models import F
from django.db.models.aggregates import Count, Sum
from django.contrib.auth.views import LoginView
from .forms import BaseOrderForm
from .services.order_creator_service import OrderCreatorService


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


class OrderCreateNewView(TemplateView):
    template_name = "orders/create.html"

    def post(self, request, *args, **kwargs):
        products = (
            request.session["products"] if "products" in request.session else None
        )
        order_service = OrderCreatorService(
            data=request.POST, user=request.user, selected_products=products
        )
        result: BaseOrderForm = order_service.create()
        if isinstance(result, BaseOrderForm):
            context = {result.form_key: result}
            return self.render_to_response(context=context)


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
