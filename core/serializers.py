from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'address', 'phone')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}  # Ensures email is required
        }

    def create(self, validated_data):
        # Use create_user method to ensure password is hashed correctly
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data)  # Correct way to create users
        if password:
            user.set_password(password)  # Set hashed password
        user.save()
        return user

    def update(self, instance, validated_data):
        # Allow partial update without forcing all fields
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def validate_username(self, value):
        if self.instance and self.instance.username == value:
            return value  # Allow the user to keep their username
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        if self.instance and self.instance.email == value:
            return value  # Allow the user to keep their email
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value
