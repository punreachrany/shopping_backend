from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Booking, Concert
from .serializers import BookingSerializer, ConcertSerializer
from users.authentication import JWTAuthentication  # Import your JWT authentication class

# API to list all concerts
class ConcertListView(APIView):
    def get(self, request):
        concerts = Concert.objects.all()
        serializer = ConcertSerializer(concerts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# API to retrieve concert by ID
class ConcertDetailView(APIView):
    def get(self, request, pk):
        concert = get_object_or_404(Concert, pk=pk)
        serializer = ConcertSerializer(concert)
        return Response(serializer.data, status=status.HTTP_200_OK)

# API to create a new concert
class ConcertCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ConcertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API to get available concerts (where seats are greater than 0)
class AvailableConcertsView(APIView):
    def get(self, request):
        available_concerts = Concert.objects.filter(seats__gt=0)
        serializer = ConcertSerializer(available_concerts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# API to book a concert by ID
class BookConcertView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        concert = get_object_or_404(Concert, pk=pk)
        num_seats = request.data.get('num_seats')

        

        # Ensure num_seats is a valid integer
        if num_seats is None or num_seats <= 0:
            return Response({'error': 'Invalid number of seats.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the concert has a valid number of seats
        if concert.seats is None:
            return Response({'error': 'Concert seats information is not available.'}, status=status.HTTP_400_BAD_REQUEST)

        if concert.seats < num_seats:
            return Response({'error': 'Not enough seats available.'}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct the number of seats
        concert.seats -= num_seats
        concert.save()

        # Create a booking entry
        booking = Booking.objects.create(user=request.user, concert=concert, num_seats=num_seats)

        total_price = concert.price * num_seats

        return Response({
            'concert_name': concert.name,
            'price_per_ticket': concert.price,
            'total_price': total_price,
            'date': concert.date_time,
            'booking_id': booking.id  # Return the booking ID for reference
        }, status=status.HTTP_200_OK)



# API to get concerts booked by the user (assumes you have a Booking model linked to User and Concert)
class UserConcertsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all bookings for the authenticated user
        user_bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(user_bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

