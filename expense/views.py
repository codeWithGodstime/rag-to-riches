from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import ExpenseSerializer, GoalSerializer
from .models import Expense, Goal


class ExpenseViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_fields = ["category"]

    def get_serializer_class(self):
        data = {
            "list": ExpenseSerializer.ExpenseRetrieveSerializer,
            "retrieve": ExpenseSerializer.ExpenseRetrieveSerializer,
            "create": ExpenseSerializer.ExpenseCreateSerializer
        }
        data.get(self.action, super().get_serializer_class())
        return data
    
    def get_queryset(self):
        qs = Expense.objects.filter(user=self.request.user)
        return qs


class GoalViewset(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["due_date", "status"]

    def get_serializer_class(self):
        data = {
            "list": GoalSerializer.GoalRetrieveSerializer,
            "retrieve": GoalSerializer.GoalRetrieveSerializer,
            "create": GoalSerializer.GoalCreateSerializer
        }
        data.get(self.action, super().get_serializer_class())
        return data

    def get_queryset(self):
        qs = Goal.objects.filter(user = self.request.user)
        return qs

