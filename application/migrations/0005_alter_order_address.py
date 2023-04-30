# Generated by Django 4.2 on 2023-04-30 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0004_alter_address_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="address",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                to="application.address",
                verbose_name="Адрес досатвки",
            ),
        ),
    ]
