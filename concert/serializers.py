from rest_framework import serializers
from .models import Concert, Booking

class ConcertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = '__all__'  # Or specify fields explicitly

# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = ['concert', 'num_seats', 'user']  # Adjust fields as needed
#         read_only_fields = ['user']  # Assuming user is set via the request

class BookingSerializer(serializers.ModelSerializer):
    concert = ConcertSerializer()  # Nest concert details

    class Meta:
        model = Booking
        fields = ['concert', 'num_seats']