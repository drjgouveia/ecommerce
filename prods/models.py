import os
import uuid
from django.db import models


def create_path(instance, filename):
    return str(os.path.join(
        str(instance.id),
        str(f"{str(uuid.uuid4()).replace('-', '_')}.{filename}")
    ))


# Create your models here.
class Product(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
