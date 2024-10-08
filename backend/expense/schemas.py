from drf_spectacular.utils import extend_schema_field, extend_schema, extend_schema_view, OpenApiParameter

from .serializers import ExpenseSerializer, GoalSerializer

EXPENSE_SCHEMA_DOCS = extend_schema_view(
    
    list=extend_schema(
        tags=["Expense"],
        summary="Retrieve all expenses for a user",
        responses={200: ExpenseSerializer.ExpenseRetrieveSerializer(many=True)}
    ),
    create=extend_schema(
        tags=["Expense"],
        request={200: ExpenseSerializer.ExpenseCreateSerializer},
        responses={200: ExpenseSerializer.ExpenseRetrieveSerializer}
    ),
    retrieve=extend_schema(
        tags=["Expense"],
        summary="retrieve a single expense by a user",
        responses={200: ExpenseSerializer.ExpenseRetrieveSerializer},
        # parameters=[
        #     OpenApiParameter(name="Expense_id", required=True, description="single expense id")
        # ]
    ),
    update=extend_schema(
        tags=["Expense"],
        request={200: ExpenseSerializer.ExpenseUpdateSerializer},
        responses={200: ExpenseSerializer.ExpenseRetrieveSerializer}
    ),
    partial_update=extend_schema(
        tags=["Expense"],
        # request={200: ExpenseSerializer.ExpenseUpdateSerializer},
        responses={200: ExpenseSerializer.ExpenseRetrieveSerializer}
    ),
    destroy=extend_schema(
        tags=["Expense"],
    )
)

GOAL_SCHEMA_DOCS = extend_schema_view(
    list=extend_schema(
        tags=["Goal"],
        summary="Retrieve all goals for a user",
        responses={200: GoalSerializer.GoalRetrieveSerializer(many=True)}
    ),
    create=extend_schema(
        tags=["Goal"],
        request={200: GoalSerializer.GoalCreateSerializer},
        responses={200: GoalSerializer.GoalRetrieveSerializer}
    ),
    retrieve=extend_schema(
        tags=["Goal"],
        summary="retrieve a single goal by a user",
        responses={200: GoalSerializer.GoalRetrieveSerializer},
        # parameters=[
        #     OpenApiParameter(name="goal_id", required=True, description="single goal id")
        # ]
    ),
    update=extend_schema(
        tags=["Goal"],
        request={200: GoalSerializer.GoalUpdateSerializer},
        responses={200: GoalSerializer.GoalRetrieveSerializer}
    ),
    partial_update=extend_schema(
        tags=["Goal"],
        # request={200: GoalSerializer.GoalUpdateSerializer},
        responses={200: GoalSerializer.GoalRetrieveSerializer}
    ),
    destroy=extend_schema(
        tags=["Goal"]
    ),
)