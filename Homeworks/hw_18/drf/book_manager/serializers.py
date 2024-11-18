"""
Define serializers for the application's models.

This module contains serializers for the `Book` and `User` models. The `BookSerializer` handles
serialization and deserialization of `Book` instances, including the creation process which
associates a book with the currently logged-in user. The `UserRegisterSerializer` facilitates
the registration of new users, ensuring that the provided passwords match and creating a new
user with the provided details.

Classes:
    - BookSerializer: Serialize and deserialize `Book` instances.
    - UserRegisterSerializer: Register a new user and validate input data.
"""

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        """
        Create a new Book instance and associate it with the logged-in user.

        :param validated_data: The validated data for creating a book.
        :type validated_data: dict
        :return: The created `Book` instance.
        :rtype: Book
        """
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}, 'email': {'required': True}}

    def validate(self, data):
        """
        Validate the input data, ensuring passwords match.

        :param data: The data to validate.
        :type data: dict
        :raises serializers.ValidationError: If passwords do not match.
        :return: The validated data.
        :rtype: dict
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        """
        Create a new User instance with the validated data.

        :param validated_data: The validated data for creating a user.
        :type validated_data: dict
        :return: The created `User` instance.
        :rtype: User
        """
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
