# Generated by Django 4.0 on 2021-12-24 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_rename_items_order_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='item',
            new_name='items',
        ),
    ]