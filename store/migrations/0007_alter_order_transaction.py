# Generated by Django 5.0.7 on 2024-09-16 20:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
        ('store', '0006_alter_order_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='checkout.transaction'),
        ),
    ]
