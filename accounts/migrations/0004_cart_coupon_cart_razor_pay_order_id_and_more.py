# Generated by Django 4.1.3 on 2022-11-27 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_coupon'),
        ('accounts', '0003_cart_cartitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.coupon'),
        ),
        migrations.AddField(
            model_name='cart',
            name='razor_pay_order_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='razor_pay_payment_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='razor_pay_payment_signature',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
