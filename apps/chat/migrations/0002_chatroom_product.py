# Generated by Django 5.1 on 2024-09-04 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0001_initial"),
        ("products", "0006_alter_category_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatroom",
            name="product",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="room",
                to="products.product",
            ),
            preserve_default=False,
        ),
    ]