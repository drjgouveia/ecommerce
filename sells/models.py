import uuid
from django.db import models


class Sell(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sell_details = models.ManyToManyField(to="sells.Sell")
    total = models.DecimalField(max_digits=7, decimal_places=2)


class SellDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(to="prods.Product", on_delete=models.SET_NULL)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=7, decimal_places=2)
