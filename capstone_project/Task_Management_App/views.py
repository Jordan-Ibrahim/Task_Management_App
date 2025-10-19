from rest_framework import generics, permissions, filters
from .models import Task
from .serializers import TaskSerializer
from Task_Management_App import serializers

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['due_date', 'priority']

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(user=user)

        # ✅ Filtering by status, priority, or due date
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        due_date = self.request.query_params.get('due_date')

        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if due_date:
            queryset = queryset.filter(due_date__date=due_date)

        return queryset


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # ✅ Only allow user to access their own tasks
        return Task.objects.filter(user=self.request.user)


class MarkTaskCompleteView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        # ✅ Mark task as complete or incomplete
        status = self.request.data.get('status')
        if status not in ['Pending', 'Completed']:
            raise serializers.ValidationError({"status": "Invalid status"})
        serializer.save(status=status)
