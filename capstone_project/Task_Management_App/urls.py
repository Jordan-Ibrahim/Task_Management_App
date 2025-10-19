from django.urls import path
from .views import TaskListCreateView, TaskDetailView, MarkTaskCompleteView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/status/', MarkTaskCompleteView.as_view(), name='task-status'),
]
