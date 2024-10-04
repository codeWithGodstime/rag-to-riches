from typing import Dict, Any

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as SimpleJWTTokenObtainPairSerializer

from .models import User
from .utils import validate_password_strength


class UserSerializer:

    class UserCreateSerializer(serializers.ModelSerializer):
        email = serializers.EmailField(
        error_messages={
            'required': 'Email is required.',
            'blank': 'Email cannot be blank.',
            'invalid': 'Please enter a valid email address.',
        }
    )
        password = serializers.CharField(
            write_only=True,
            error_messages={
                'required': 'Password is required.',
                'blank': 'Password cannot be blank.',
            }
    )
        class Meta:
            model=User
            fields = ("email", "password")

        def is_valid(self, raise_exception=False):
            """
            Override the is_valid method to return plain error messages.
            """
            try:
                return super().is_valid(raise_exception=raise_exception)
            except ValidationError as exc:
                # Format errors to remove the ErrorDetail
                exc.detail = {"errors": {field: str(message[0]) for field, message in exc.detail.items()}}
                if raise_exception:
                    raise exc
                return False
        
        def validate_password(self, password):
            data = validate_password_strength(password)
            return data

        def create(self, validated_data):
            user = User(email=validated_data['email'])
            user.set_password(validated_data['password'])
            user.save()
            return user
        

    class UserRetrieveSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = (
                "id", 
                "email", 
                "first_name",
                "last_name",
                "profile_picture",
                "bio",
                "address",
                "created_at",
                "updated_at"
            )

    class UserResetPasswordSerializer(serializers.Serializer):
        email = serializers.EmailField()

        def validate_email(self, value):
            # Check if the user with this email exists
            if not User.objects.filter(email=value).exists():
                raise serializers.ValidationError("User with this email does not exist.")
            return value
        
    class UserResetPasswordConfirmationSerializer(serializers.Serializer):
        uid = serializers.CharField(max_length=999)
        token = serializers.CharField(max_length=999)
        new_password = serializers.CharField(max_length=40)

        def validate_new_password(self, password):
            data = validate_password_strength(password)
            return data
        
    class UserChangePasswordSerializer(serializers.Serializer):
        current_password = serializers.CharField(max_length=30)
        new_password = serializers.CharField(max_length=30)

        def validate_new_password(self, password):
            data = validate_password_strength(password)
            return data
        
    class UserVerificationSerializer(serializers.Serializer):
        uid = serializers.CharField(max_length=999)
        token = serializers.CharField(max_length=999)
        

class TokenObtainSerializer(SimpleJWTTokenObtainPairSerializer):

    def validate(self, attrs: Dict[str, Any]):

        data = super().validate(attrs)

        user = self.user
        # Check if the user account is active
        if not user.is_active:
            raise serializers.ValidationError('User account is inactive.')
        
        if not user.is_verified:
            print("react")
            raise serializers.ValidationError('User account is has not yet been verified.')
        
        user_data = UserSerializer.UserRetrieveSerializer(user).data
        
        data['message'] = "you've successfully logged in"
        data['data'] = user_data
        return data
    
    def is_valid(self, raise_exception=False):
            """
            Override the is_valid method to return plain error messages.
            """
            try:
                return super().is_valid(raise_exception=raise_exception)
            except ValidationError as exc:
                exc.detail = {"errors": {field: str(message[0]) for field, message in exc.detail.items()}}
                if raise_exception:
                    raise exc
                return False