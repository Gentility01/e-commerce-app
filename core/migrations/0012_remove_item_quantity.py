# Generated by Django 4.0 on 2021-12-24 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_rename_item_order_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
    ]
