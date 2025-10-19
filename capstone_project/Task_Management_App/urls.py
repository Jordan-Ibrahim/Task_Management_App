from django.urls import path
from .views import TaskListCreateView, TaskDetailView, MarkTaskCompleteView, RegisterView, LoginView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/status/', MarkTaskCompleteView.as_view(), name='task-status'),
    path('users/register/', RegisterView.as_view(), name='user-register'),
    path('users/login/', LoginView.as_view(), name='user-login'),
]
