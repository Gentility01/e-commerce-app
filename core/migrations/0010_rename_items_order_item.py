# Generated by Django 4.0 on 2021-12-24 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_orderitem_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='items',
            new_name='item',
        ),
    ]
