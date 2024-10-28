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
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    out_of_stock = models.BooleanField(default=False)
    image_url = models.URLField(
        max_length=300, 
        blank=True, 
        null=True, 
        default="https://avatars.githubusercontent.com/u/54469196?s=400&u=c6efe15c16cba57e6aee56b60502ac0f5e5950ec&v=4"
    )

    def __str__(self):
        return self.name
