import base64

from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError


def validate_password_strength(password):
    """Validate password strength."""
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must contain at least one digit.")
    if not any(char.isalpha() for char in password):
        raise ValidationError("Password must contain at least one letter.")
    if not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?/`~' for char in password):
        raise ValidationError("Password must contain at least one special character.")
    return password

def generate_token_link(user, action):
    """
    Generates a link with a token for different actions (email verification, password reset, etc.)
    
    :param user: The user instance.
    :param action: The action for the link ('email_verify', 'password_reset', etc.).
                   This should match the corresponding URL name in `urls.py`.
    :return: The full URL link with the token.
    """
    # Encode the user's primary key

    user_id = str(user.id)
    value_bytes = user_id.encode('utf-8')
    encoded_value = base64.urlsafe_b64encode(value_bytes)
    encoded_string = encoded_value.decode('utf-8')
    # uid = urlsafe_base64_encode(force_bytes(user.id))
    uid = encoded_string
    
    # Generate a token using the default token generator
    token = default_token_generator.make_token(user)
    
    # Generate the URL based on the action provided
    url = f"/{action}/{uid}/{token}"
    
    # Build the full URL (adjust the domain as needed)
    genrated_link = f"http://{settings.FRONTEND_DOMAIN}{url}"
    
    return genrated_link

def generate_password_reset_message(user, reset_link):
    """
    Generates a password reset message with the provided reset link.
    
    :param user: The user instance for whom the password reset is generated.
    :param reset_link: The URL link for password reset.
    :return: A string containing the password reset message.
    """
    message = f"""
    Hi User,

    We received a request to reset your password. Please click the link below to reset your password:

    {reset_link}

    If you did not request a password reset, please ignore this email or contact support if you have any questions.

    Thanks,
    The YourWebsite Team
    """
    return message

def verify_email_token(uid, token):
    from django.contrib.auth import get_user_model
    try:
        # Base64 decode the uid
        decoded_bytes = base64.urlsafe_b64decode(uid)
        user_id = decoded_bytes.decode('utf-8')  # Convert bytes back to string
        
        # Fetch the user based on the decoded user ID
        user = get_user_model().objects.get(id=user_id)
        
        # Check the validity of the token
        if default_token_generator.check_token(user, token):
            return user  # Token is valid, return the user instance
        else:
            return None  # Token is invalid
    except (ValueError, ObjectDoesNotExist):
        return None  # Invalid UID or user does not exist
