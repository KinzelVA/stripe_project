#payments/models.py
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")

    def __str__(self):
        return self.name

class Order(models.Model):
    items = models.ManyToManyField(Item, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        """Пересчитывает сумму заказа"""
        self.total_amount = sum(item.price for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Order {self.id} - {self.total_amount} {self.items.first().currency if self.items.exists() else 'USD'}"
