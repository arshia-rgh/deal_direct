# Generated by Django 5.1 on 2024-08-25 12:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0001_initial"),
        ("orders", "0005_alter_order_cart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="cart",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order",
                to="cart.cart",
            ),
        ),
    ]