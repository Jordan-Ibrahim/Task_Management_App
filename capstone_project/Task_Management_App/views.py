from rest_framework import generics, permissions, filters
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# User Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# User Login (optional simple version)
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})


# Task Views
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]


class MarkTaskCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
            task.is_completed = True
            task.save()
            return Response({"message": "Task marked as complete"}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
