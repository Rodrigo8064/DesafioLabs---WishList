from django.conf import settings
from django.db import models


class Favorite(models.Model):
    product = models.ForeignKey(
        'products.Product', on_delete=models.CASCADE, related_name='favorite'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_favorites',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
