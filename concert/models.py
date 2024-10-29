from django.db import models

from users.models import User

class Concert(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    venue = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    seats = models.PositiveIntegerField(default=0)  # Ensure this has a default
    price = models.FloatField()
    image_url = models.URLField(default="https://avatars.githubusercontent.com/u/54469196?s=400&u=c6efe15c16cba57e6aee56b60502ac0f5e5950ec&v=4")
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='bookings')
    num_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.email} booked {self.num_seats} seats for {self.concert.name}"
