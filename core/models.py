from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, blank=False, null=True, max_length=300)
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=300, blank=False, null=True)
    last_name = models.CharField(max_length=300, blank=False, null=True)
    # role = None
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    profile_picture = models.ImageField(blank=True, default="default.jpg")
    bio = models.TextField(null=True, blank=True)
    # country = models.CharField() # change to django_coutries
    # state = models.CharField()
    address = models.CharField(max_length=500, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)



