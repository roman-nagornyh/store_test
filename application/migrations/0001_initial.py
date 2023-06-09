# Generated by Django 4.2 on 2023-04-29 08:20

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "phone",
                    models.CharField(max_length=11, verbose_name="Номер телефона"),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
                "db_table": "users",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city", models.CharField(max_length=100, verbose_name="Город")),
                ("street", models.CharField(max_length=100, verbose_name="Улица")),
                ("house", models.CharField(max_length=10, verbose_name="Дом")),
                ("entrance", models.IntegerField(verbose_name="Подъезд")),
                ("apartment", models.IntegerField(verbose_name="Квартира")),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Адрес доставки",
                "verbose_name_plural": "Адреса доставки",
                "db_table": "addresses",
            },
        ),
        migrations.CreateModel(
            name="OrderStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Статус заказа",
                "verbose_name_plural": "Статусы заказов",
                "db_table": "order_statuses",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Наименование")),
                ("price", models.FloatField(verbose_name="Цена")),
                ("count", models.IntegerField(verbose_name="Количество товара")),
            ],
            options={
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
                "db_table": "products",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа"),
                ),
                (
                    "date_receiving",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Дата получения"
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=11, verbose_name="Номер мобильного телефона"
                    ),
                ),
                (
                    "address",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="application.address",
                        verbose_name="Адрес досатвки",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="application.orderstatus",
                        verbose_name="Статус заказа",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заказ",
                "verbose_name_plural": "Заказы",
                "db_table": "orders",
            },
        ),
        migrations.CreateModel(
            name="Bucket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="application.product",
                        verbose_name="Товар",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Корзина",
                "verbose_name_plural": "Корзина",
                "db_table": "buckets",
            },
        ),
    ]
