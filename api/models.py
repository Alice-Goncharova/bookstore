from django.contrib.auth.models import AbstractUser
from django.db import models


class ApiUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('supplier', 'Supplier'),
        ('consumer', 'Consumer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    ...


class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.id}: {self.warehouse_name}"


class Product(models.Model):
    name = models.CharField(max_length=128)
    warehouse = models.ForeignKey(Warehouse, related_name='products', \
                                  on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    def ship(self, count):
        count = int(count)
        if count < 0:
            raise ValueError("You can't receive products")
        self.count += count
        self.save()

    def receive(self, count):
        count = int(count)
        if count < 0:
            raise ValueError("You can't ship products")
        if count > self.count:
            raise ValueError("Not enough products in stock")
        self.count -= count
        self.save()

    def __str__(self):
        return f"{self.warehouse.warehouse_name}. Product: {self.name}"


