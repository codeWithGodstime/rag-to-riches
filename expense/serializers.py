from rest_framework import serializers
from .models import Goal, Expense, Category

class ExpenseSerializer:
    class ExpenseCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Expense
            fields = ("title", "description", "amount", "user", "category")

    class ExpenseUpdateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Expense
            fields = ("title", "description", "amount", "category")

    class ExpenseRetrieveSerializer(ExpenseCreateSerializer):
        ...


class GoalSerializer:
    class GoalCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Goal
            fields = ("title", "due_date", "status", "user", "estimated_amount", "priority")

    class GoalUpdateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Goal
            fields = ("title", "due_date", "status", "estimated_amount", "priority")

    class GoalRetrieveSerializer(GoalCreateSerializer):
        ...