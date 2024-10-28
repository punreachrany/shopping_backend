from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Foods', 'Foods'),
        ('Clothes', 'Clothes'),
        ('Electronics', 'Electronics'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    quantity = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)  # New field
    out_of_stock = models.BooleanField(default=False)  # New field
    image_url = models.URLField(max_length=300, blank=True, null=True)  # New field

    def __str__(self):
        return self.name