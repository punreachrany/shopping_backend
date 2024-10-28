from datetime import datetime, timedelta, timezone
from django.shortcuts import get_object_or_404
import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated  # Import to use for user authentication
from users.models import User
from .serializers import UserSerializer
from .authentication import JWTAuthentication  # Import your JWTAuthentication class

# Helper function to generate JWT tokens
def generate_jwt(user):
    payload = {
        'id': user.id,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=60),
        'iat': datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token

# View for user registration
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Save the user and get the instance

        # Generate JWT token for the new user
        token = generate_jwt(user)

        response = Response(
            {'status': 'success', 'jwt': token}, 
            status=201
        )
        response.set_cookie(key='jwt', value=token, httponly=True)  # Set cookie with JWT
        return response

# View for user login
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = get_object_or_404(User, email=email)

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        token = generate_jwt(user)

        response = Response(
            {'status': 'success', 'jwt': token}, 
            status=200
        )
        response.set_cookie(key='jwt', value=token, httponly=True)  # Set JWT as HttpOnly cookie
        return response

# View to get authenticated user details
class UserView(APIView):
    authentication_classes = [JWTAuthentication]  # Use your JWT authentication class
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def get(self, request):
        user = request.user  # User is already authenticated, we can directly access it
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

# View for user logout
class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]  # Use your JWT authentication class
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def post(self, request):
        response = Response({'message': 'success'}, status=200)
        response.delete_cookie('jwt')
        return response

# New View to check if the user is logged in
class IsLoggedInView(APIView):
    authentication_classes = [JWTAuthentication]  # Use your JWT authentication class
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def get(self, request):
        user = request.user  # Get the authenticated user
        token = generate_jwt(user)  # Generate a new token if needed
        return Response({'is_logged_in': True, 'jwt': token}, status=200)