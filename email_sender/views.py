from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response


class SendEmailView(APIView):
    def post(self, request):
        subject = request.data.get('subject', 'No Subject')  # Use request.data
        message = request.data.get('message', 'No Message')
        recipient_list = request.data.get('recipient_list', [])  # Expecting a list

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=False,
            )
            return Response({'status': 'success', 'message': 'Email sent successfully!'})
        except Exception as e:
            return Response({'status': 'failed', 'message': str(e)})
