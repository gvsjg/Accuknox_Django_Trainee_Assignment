from django.db import models

# Create your models here.
from typing import Iterator, Dict

class Rectangle(models.Model):
    length = models.IntegerField()
    width = models.IntegerField()

    def __iter__(self) -> Iterator[Dict[str, int]]:
        yield {'length': self.length}
        yield {'width': self.width}

    def __str__(self):
        return f"Rectangle (Length: {self.length}, Width: {self.width})"

    def save(self, *args, **kwargs):
        if not isinstance(self.length, int) or not isinstance(self.width, int):
            raise TypeError("Length and width must be integers.")
        if self.length <= 0 or self.width <= 0:
            raise ValueError("Length and width must be positive.")
        super().save(*args, **kwargs)