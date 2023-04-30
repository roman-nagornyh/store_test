# Generated by Django 4.2 on 2023-04-30 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0002_productorder"),
    ]

    operations = [
        migrations.AddField(
            model_name="productorder",
            name="count",
            field=models.IntegerField(default=1, verbose_name="Количество"),
        ),
        migrations.AlterField(
            model_name="productorder",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="products_orders",
                to="application.order",
                verbose_name="Заказ",
            ),
        ),
    ]
