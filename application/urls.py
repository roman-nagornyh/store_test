from django.urls import path
from .views import (
    ProductList,
    add_product_bucket,
    BucketView,
    OrderCreateView,
    OrderListView,
    product_subtraction,
    product_delete,
)

app_name = "application"

urlpatterns = [
    path("", ProductList.as_view(), name="products"),
    path("bucket_add/<int:product_id>/", add_product_bucket, name="bucket_add"),
    path("bucket/", BucketView.as_view(), name="bucket"),
    path(
        "bucket/product_subtraction/<int:product_id>",
        product_subtraction,
        name="product_subtraction",
    ),
    path(
        "bucket/product_delete/<int:product_id>", product_delete, name="product_delete"
    ),
    path("order/create", OrderCreateView.as_view(), name="order_create"),
    path("order/list", OrderListView.as_view(), name="order_list"),
]
