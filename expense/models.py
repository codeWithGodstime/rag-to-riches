import uuid

from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): self.name


class Expense(models.Model):

    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        default="miscellenous"
    )

    def __str__(self): self.title


class Goal(models.Model):

    status = (
        ("done", "DONE"),
        ("pending", "PENDING")
    )

    priority = ((i, i) for i in range(5))

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=status)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    estimated_amount = models.DecimalField(max_digits=14, decimal_places=2)
    priority = models.CharField(max_length=1, choices=priority)

    def __str__(self): return self.title
