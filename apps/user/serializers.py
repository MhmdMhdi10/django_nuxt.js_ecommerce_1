from rest_framework import serializers
import re
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserCreateSerializer
from ecommerce.settings import AUTH_USER_MODEL
User = AUTH_USER_MODEL


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'phone_number', 'is_active', 'is_staff')

    def validate_phone_number(self, value):
        """
        Check that the phone number is in a valid format
        """
        phone_regex = r'^(\+989|09)\d{9}$'
        if not re.match(phone_regex, value):
            raise serializers.ValidationError(
                _("Phone number must be entered in the format: '+989xxxxxxxxx' or '09xxxxxxxxx'."))
        return value

    def create(self, validated_data):
        """
        Create and return a new UserAccount instance, given the validated data
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing UserAccount instance, given the validated data
        """
        instance.username = validated_data.get('username', instance.username)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()
        return instance
