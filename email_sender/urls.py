# email_sender/urls.py
from django.urls import path
from .views import SendEmailView

urlpatterns = [
    path('inquiry/', SendEmailView.as_view(), name='send_email'),
]
