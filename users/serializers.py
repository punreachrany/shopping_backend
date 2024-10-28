from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'birthday', 'gender', 'profile_url']  # Added profile_url
        extra_kwargs = {
            'password': {'write_only': True},  # Password should only be set, not returned
            'profile_url': {'read_only': True},  # Make profile_url read-only
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)  # Set the password in a hashed format
        instance.save()
        return instance
