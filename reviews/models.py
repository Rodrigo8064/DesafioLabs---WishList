from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from products.models import Product


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews'
    )
    stars = models.IntegerField(
        validators=[
            MinValueValidator(0, 'Avaliação não pode ser inferior a 0'),
            MaxValueValidator(5, 'Avaliação nao pode ser superior a 5'),
        ]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'
