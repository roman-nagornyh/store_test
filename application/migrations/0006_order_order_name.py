# Generated by Django 4.2 on 2023-04-30 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0005_alter_order_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_name",
            field=models.CharField(
                default="", max_length=100, verbose_name="Имя заказчика"
            ),
        ),
    ]
