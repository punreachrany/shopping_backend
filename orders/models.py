from django.db import models
from users.models import User
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # New field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.product.name} ({self.quantity} units)"
    
class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_list = models.ManyToManyField(Order)  # Many-to-many relationship with Order
    date = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"OrderHistory for {self.user.email} on {self.date}"