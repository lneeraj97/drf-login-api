from rest_framework import serializers
from . import models


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        # Add id here
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password',
                }
            }
        }

    def create(self, validated_data):
        """ Overrides the default create function """
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """ Handles updating a user model """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserStatus
        fields = '__all__'
        extra_kwargs = {
            'user_profile': {
                'read_only': True
            },
            'date_created': {
                'read_only': True
            }
        }
