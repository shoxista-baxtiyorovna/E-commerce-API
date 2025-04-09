from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):

    KUTILMOQDA = 'kutilmoqda'
    JARAYONDA = 'jarayonda'
    YUBORILGAN = 'yuborilgan'
    YETKAZILGAN = 'yetkazilgan'
    BEKOR_QILINGAN = 'bekor qilingan'

    ORDER_STATUS_CHOICES = [
        (KUTILMOQDA, 'Kutilmoqda'),
        (JARAYONDA, 'Jarayonda'),
        (YUBORILGAN, 'Yuborilgan'),
        (YETKAZILGAN, 'Yetkazilgan'),
        (BEKOR_QILINGAN, 'Bekor qilingan'),
    ]


    BY_CARD = 'by card'
    PAYPAL = 'PayPal'
    WITH_BANK = 'with bank'
    COD = 'COD'

    PAYMENT_METHOD_CHOICES = [
        (BY_CARD, 'Kredit karta'),
        (PAYPAL, 'PayPal'),
        (WITH_BANK, "Bank o'tkazmasi"),
        (COD, "Yetkazib berishda to'lash"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default=KUTILMOQDA)
    shipping_address = models.TextField()
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default=BY_CARD)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()

    @property
    def total_price(self):
        return sum(order.total_price for order in(self.product.price * self.quantity))
