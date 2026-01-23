from django.urls import path
from .views import plan_day

urlpatterns = [
    path("plan-day/", plan_day),
]
