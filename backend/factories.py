import factory

from core.models import User
from expense.models import Expense, Goal, Category


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category


class ExpenseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Expense

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal
    
    user = factory.SubFactory(UserFactory)


