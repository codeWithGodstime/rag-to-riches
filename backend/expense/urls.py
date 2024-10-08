from rest_framework.routers import SimpleRouter

from .views import ExpenseViewset, GoalViewset

router = SimpleRouter()
router.register("expenses", ExpenseViewset, "expenses")
router.register("goals", GoalViewset, "goals")

urlpatterns = router.urls