from django.db import models
from store.models import Product

# Create your models here.

class Basket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='baskets')
    quantity = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product},{self.quantity},{self.created_date}'