from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    brand = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
