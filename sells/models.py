import uuid
from django.db import models
from django.contrib.auth.models import User


class Sell(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    sell_details = models.ManyToManyField(to="sells.SellDetails")
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)


class SellDetails(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True, editable=False)
    product = models.ForeignKey(to="prods.Product", on_delete=models.SET_NULL, null=True)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.DecimalField(max_digits=7, decimal_places=2)
