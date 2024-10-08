# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import ExpenseSerializer, GoalSerializer
from .models import Expense, Goal
from .schemas import GOAL_SCHEMA_DOCS, EXPENSE_SCHEMA_DOCS


@EXPENSE_SCHEMA_DOCS
class ExpenseViewset(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_fields = ["category"]
    serializer_class = ExpenseSerializer.ExpenseRetrieveSerializer

    def get_serializer_class(self):
        data = {
            "list": ExpenseSerializer.ExpenseRetrieveSerializer,
            "retrieve": ExpenseSerializer.ExpenseRetrieveSerializer,
            "create": ExpenseSerializer.ExpenseCreateSerializer
        }
        data.get(self.action)
        return data or super().get_serializer_class()
    
    def get_queryset(self):
        qs = Expense.objects.filter(user=self.request.user)
        return qs

@GOAL_SCHEMA_DOCS
class GoalViewset(viewsets.ModelViewSet):
    queryset = Goal.objects.none()
    serializer_class = GoalSerializer.GoalRetrieveSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["due_date", "status"]

    def get_serializer_class(self):
        data = {
            "list": GoalSerializer.GoalRetrieveSerializer,
            "retrieve": GoalSerializer.GoalRetrieveSerializer,
            "create": GoalSerializer.GoalCreateSerializer
        }
        data.get(self.action)
        return data or super().get_serializer_class()

    def get_queryset(self):
        qs = Goal.objects.filter(user = self.request.user)
        return qs

