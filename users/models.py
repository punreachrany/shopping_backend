from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    birthday = models.DateField(null=True, blank=True)  # New field
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        null=True,
        blank=True
    )  # New field
    username = None  # Remove username field
    profile_url = models.URLField(
        max_length=300, 
        blank=True, 
        null=True, 
        default="https://avatars.githubusercontent.com/u/54469196?s=400&u=c6efe15c16cba57e6aee56b60502ac0f5e5950ec&v=4"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
