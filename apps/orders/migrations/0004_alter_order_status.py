# Generated by Django 5.1 on 2024-08-24 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("S", "Sending"),
                    ("C", "Completed"),
                    ("W", "Waiting For Payment"),
                ],
                default="W",
                max_length=255,
            ),
        ),
    ]