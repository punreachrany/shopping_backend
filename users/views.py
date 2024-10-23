from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from users.models import User
from .serializers import UserSerializer
import jwt
from datetime import datetime, timedelta, timezone


# Helper function to generate JWT tokens
def generate_jwt(user):
    payload = {
        'id': user.id,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=60),
        'iat': datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token


# Helper function to decode JWT tokens
def decode_jwt(token):
    try:
        return jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')


# View for user registration
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


# View for user login
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = get_object_or_404(User, email=email)

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        token = generate_jwt(user)

        response = Response({'jwt': token}, status=200)
        response.set_cookie(key='jwt', value=token, httponly=True)
        return response


# View to get authenticated user details
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        payload = decode_jwt(token)

        user = get_object_or_404(User, id=payload['id'])
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


# View for user logout
class LogoutView(APIView):
    def post(self, request):
        response = Response({'message': 'success'}, status=200)
        response.delete_cookie('jwt')
        return response