from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.authentication import JWTAuthentication

class SendEmailView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user  # Get the logged-in user
        title = request.data.get('title', 'No Title Provided')
        message = request.data.get('message', 'No message provided.')

        # Prepare the email body
        email_body = f"""
        User Info:
        Name: {user.name}
        Email: {user.email}
        ID: {user.id}

        Message:
        {message}
        """

        subject = f'Shopping Inquiry from {user.email} - {title}'

        try:
            send_mail(
                subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            return Response({'status': 'success', 'message': 'Email sent successfully!'})
        except Exception as e:
            return Response({'status': 'failed', 'message': str(e)})
