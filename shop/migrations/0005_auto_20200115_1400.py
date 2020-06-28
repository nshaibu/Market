# Generated by Django 3.0.2 on 2020-01-15 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_item_total_in_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('PENDING', 'pending'), ('ORDERED', 'ordered'), ('DELIVERED', 'deliver'), ('RECEIVED', 'received')], max_length=30),
        ),
    ]